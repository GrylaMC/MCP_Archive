import jpype
import jpype.imports
from jpype.types import *
import os
import zipfile
import uuid
import urllib.request
import sys
import pickle
import argparse

# --- CONFIGURATION ---
ASM_VERSION = "9.7"
MAVEN_REPO = "https://repo1.maven.org/maven2/org/ow2/asm"
JARS = ["asm", "asm-tree", "asm-commons"]
LIB_DIR = "./lib"
REGISTRY_FILE = "registry.pkl"

# --- SETUP JAVA ENVIRONMENT ---
def setup_dependencies():
    if not os.path.exists(LIB_DIR):
        os.makedirs(LIB_DIR)
    
    classpath = []
    for jar in JARS:
        filename = f"{jar}-{ASM_VERSION}.jar"
        path = os.path.join(LIB_DIR, filename)
        if not os.path.exists(path):
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(f"{MAVEN_REPO}/{jar}/{ASM_VERSION}/{filename}", path)
        classpath.append(path)
    return classpath

def init_jvm():
    if not jpype.isJVMStarted():
        classpath = setup_dependencies()
        jpype.startJVM(classpath=classpath)

init_jvm()

# Import ASM classes
from org.objectweb.asm import Opcodes, ClassReader, ClassWriter
from org.objectweb.asm.tree import ClassNode, MethodNode, FieldNode, \
    MethodInsnNode, FieldInsnNode, LdcInsnNode, TypeInsnNode, InsnNode
from jpype import JArray, JByte

# --- PHASE 1: TAINTING ---

REGISTRY = { "classes": {}, "methods": {}, "fields": {} }
def taint_jar(input_jar_path, output_jar_path):
    print(f"[*] Tainting {input_jar_path} -> {output_jar_path}")

    global REGISTRY
    REGISTRY = { "classes": {}, "methods": {}, "fields": {} }
    
    with zipfile.ZipFile(input_jar_path, 'r') as zin, \
         zipfile.ZipFile(output_jar_path, 'w') as zout:
        
        for item in zin.infolist():
            if not item.filename.endswith(".class"):
                zout.writestr(item, zin.read(item.filename))
                continue

            bytes_in = zin.read(item.filename)
            jbytes = JArray(JByte)(bytes_in)
            
            try:
                cr = ClassReader(jbytes)
                cn = ClassNode()
                cr.accept(cn, 0)
            except Exception as e:
                print(f"Failed to parse {item.filename}: {e}")
                zout.writestr(item, bytes_in)
                continue
            
            # FIX: Cast Java String to Python str()
            original_owner = str(cn.name)

            # 1. MARK CLASS
            c_uid = str(uuid.uuid4())
            REGISTRY["classes"][c_uid] = {"name": original_owner}
            
            trace_field = FieldNode(
                Opcodes.ACC_PUBLIC | Opcodes.ACC_STATIC | Opcodes.ACC_FINAL,
                "__MCP_UUID__", "Ljava/lang/String;", None, c_uid
            )
            cn.fields.add(trace_field)

            # 2. MARK FIELDS
            for field in list(cn.fields):
                if field.name == "__MCP_UUID__": continue
                
                f_uid = str(uuid.uuid4()).replace("-", "")
                
                # FIX: Cast Java Strings to Python str()
                REGISTRY["fields"][f_uid] = {
                    "owner": original_owner, 
                    "name": str(field.name), 
                    "desc": str(field.desc)
                }

                mw = MethodNode(Opcodes.ACC_PUBLIC | Opcodes.ACC_STATIC, 
                                f"$$mcp_trace_{f_uid}", "()V", None, None)
                
                is_static = (field.access & Opcodes.ACC_STATIC) != 0
                if not is_static: mw.instructions.add(InsnNode(Opcodes.ACONST_NULL))
                
                mw.instructions.add(FieldInsnNode(
                    Opcodes.GETSTATIC if is_static else Opcodes.GETFIELD, 
                    cn.name, field.name, field.desc
                ))
                mw.instructions.add(InsnNode(Opcodes.POP))
                mw.instructions.add(InsnNode(Opcodes.RETURN))
                cn.methods.add(mw)

            # 3. MARK METHODS
            for method in cn.methods:
                if str(method.name).startswith("<") or str(method.name).startswith("$$mcp"): continue
                if (method.access & Opcodes.ACC_ABSTRACT) or (method.access & Opcodes.ACC_NATIVE): continue

                m_uid = str(uuid.uuid4())
                
                # FIX: Cast Java Strings to Python str()
                REGISTRY["methods"][m_uid] = {
                    "owner": original_owner, 
                    "name": str(method.name), 
                    "desc": str(method.desc)
                }

                method.instructions.clear()
                method.tryCatchBlocks.clear()
                method.localVariables.clear()
                method.instructions.add(TypeInsnNode(Opcodes.NEW, "java/lang/Error"))
                method.instructions.add(InsnNode(Opcodes.DUP))
                method.instructions.add(LdcInsnNode(m_uid))
                method.instructions.add(MethodInsnNode(
                    Opcodes.INVOKESPECIAL, "java/lang/Error", "<init>", "(Ljava/lang/String;)V", False
                ))
                method.instructions.add(InsnNode(Opcodes.ATHROW))

            cw = ClassWriter(ClassWriter.COMPUTE_MAXS)
            cn.accept(cw)
            zout.writestr(item.filename, cw.toByteArray())


# --- PHASE 2: EXTRACTION ---

def generate_tiny(remapped_jar_path, output_tiny_path):
    print(f"[*] Analyzing {remapped_jar_path} -> {output_tiny_path}")
    global REGISTRY
    
    tiny_lines = ["v1\tofficial\tnamed"]
    matches_found = 0

    with zipfile.ZipFile(remapped_jar_path, 'r') as z:
        for filename in z.namelist():
            if not filename.endswith(".class"): continue
            
            bytes_in = z.read(filename)
            jbytes = JArray(JByte)(bytes_in)
            
            try:
                cr = ClassReader(jbytes)
                cn = ClassNode()
                cr.accept(cn, 0)
            except Exception:
                continue

            # 1. RESOLVE CLASSES
            c_uid = None
            for field in cn.fields:
                if str(field.name) == "__MCP_UUID__":
                    c_uid = str(field.value) # Convert to python string for dict lookup
                    break
            
            if not c_uid: continue
            
            orig_c_data = REGISTRY["classes"].get(c_uid)
            if not orig_c_data: continue

            matches_found += 1
            original_c_name = orig_c_data["name"]
            mapped_c_name = str(cn.name)
            tiny_lines.append(f"CLASS\t{original_c_name}\t{mapped_c_name}")

            # 2. RESOLVE FIELDS
            for method in cn.methods:
                method_name = str(method.name)
                if method_name.startswith("$$mcp_trace_"):
                    f_uid = method_name.replace("$$mcp_trace_", "")
                    
                    insn = method.instructions.getFirst()
                    while insn:
                        if isinstance(insn, FieldInsnNode):
                            mapped_f_name = str(insn.name)
                            orig_f_data = REGISTRY["fields"].get(f_uid)
                            
                            if orig_f_data:
                                tiny_lines.append(
                                    f"FIELD\t{original_c_name}\t{orig_f_data['desc']}\t{orig_f_data['name']}\t{mapped_f_name}"
                                )
                            break
                        insn = insn.getNext()

            # 3. RESOLVE METHODS
            for method in cn.methods:
                insn = method.instructions.getFirst()
                while insn:
                    # Note: LdcInsnNode.cst can be String, Type, etc.
                    if isinstance(insn, LdcInsnNode) and isinstance(insn.cst, str): 
                        m_uid = str(insn.cst) # Ensure python string
                        if m_uid in REGISTRY["methods"]:
                            orig_m_data = REGISTRY["methods"][m_uid]
                            mapped_m_name = str(method.name)
                            tiny_lines.append(
                                f"METHOD\t{original_c_name}\t{orig_m_data['desc']}\t{orig_m_data['name']}\t{mapped_m_name}"
                            )
                        break
                    insn = insn.getNext()

    with open(output_tiny_path, "w") as f:
        f.write("\n".join(tiny_lines))
    print(f"[*] Done. Matches Found: {matches_found}. File written to {output_tiny_path}")

