import jpype
import jpype.imports
from jpype.types import *
import os
import zipfile
import uuid
import urllib.request
import sys
from collections import defaultdict

# --- CONFIGURATION ---
ASM_VERSION = "9.7"
MAVEN_REPO = "https://repo1.maven.org/maven2/org/ow2/asm"
JARS = ["asm", "asm-tree", "asm-commons"]
LIB_DIR = "./lib"

# --- SETUP JAVA ENVIRONMENT ---
def setup_dependencies():
    if not os.path.exists(LIB_DIR):
        os.makedirs(LIB_DIR)
    
    classpath = []
    for jar in JARS:
        filename = f"{jar}-{ASM_VERSION}.jar"
        path = os.path.join(LIB_DIR, filename)
        if not os.path.exists(path):
            url = f"{MAVEN_REPO}/{jar}/{ASM_VERSION}/{filename}"
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, path)
        classpath.append(path)
    return classpath

def init_jvm():
    if not jpype.isJVMStarted():
        classpath = setup_dependencies()
        jpype.startJVM(classpath=classpath)

init_jvm()

# Import ASM classes after JVM start
from org.objectweb.asm import Opcodes, ClassReader, ClassWriter
from org.objectweb.asm.tree import ClassNode, MethodNode, FieldNode, \
    MethodInsnNode, FieldInsnNode, LdcInsnNode, TypeInsnNode, InsnNode
from jpype import JArray, JByte

# --- DATA STRUCTURES ---
REGISTRY = {
    "classes": {},
    "methods": {},
    "fields": {}
}

# --- PHASE 1: TAINTING ---

def taint_jar(input_jar_path, output_jar_path):
    print(f"[*] Tainting {input_jar_path} -> {output_jar_path}")
    
    with zipfile.ZipFile(input_jar_path, 'r') as zin, \
         zipfile.ZipFile(output_jar_path, 'w') as zout:
        
        for item in zin.infolist():
            if not item.filename.endswith(".class"):
                zout.writestr(item, zin.read(item.filename))
                continue

            # Read Class
            bytes_in = zin.read(item.filename)
            
            # FIX: Explicitly cast Python bytes to Java byte[] to hit the correct constructor
            jbytes = JArray(JByte)(bytes_in)
            
            try:
                cr = ClassReader(jbytes)
                cn = ClassNode()
                cr.accept(cn, 0)
            except Exception as e:
                print(f"Failed to read {item.filename}: {e}")
                zout.writestr(item, bytes_in)
                continue
            
            original_owner = cn.name

            # 1. MARK CLASS (Static Field)
            c_uid = str(uuid.uuid4())
            REGISTRY["classes"][c_uid] = {"name": original_owner}
            
            trace_field = FieldNode(
                Opcodes.ACC_PUBLIC | Opcodes.ACC_STATIC | Opcodes.ACC_FINAL,
                "__MCP_UUID__",
                "Ljava/lang/String;",
                None,
                c_uid
            )
            cn.fields.add(trace_field)

            # 2. MARK FIELDS (Via Synthetic Methods)
            # Create copy of fields list to avoid ConcurrentModification during iteration
            original_fields = list(cn.fields)
            
            for field in original_fields:
                if field.name == "__MCP_UUID__": continue
                
                f_uid = str(uuid.uuid4()).replace("-", "")
                REGISTRY["fields"][f_uid] = {
                    "owner": original_owner,
                    "name": field.name, 
                    "desc": field.desc
                }

                trace_method_name = f"$$mcp_trace_{f_uid}"
                mw = MethodNode(
                    Opcodes.ACC_PUBLIC | Opcodes.ACC_STATIC, 
                    trace_method_name, 
                    "()V", 
                    None, 
                    None
                )
                
                is_static = (field.access & Opcodes.ACC_STATIC) != 0
                opcode = Opcodes.GETSTATIC if is_static else Opcodes.GETFIELD
                
                if not is_static:
                    mw.instructions.add(InsnNode(Opcodes.ACONST_NULL))
                
                mw.instructions.add(FieldInsnNode(opcode, cn.name, field.name, field.desc))
                mw.instructions.add(InsnNode(Opcodes.POP))
                mw.instructions.add(InsnNode(Opcodes.RETURN))
                
                cn.methods.add(mw)

            # 3. MARK METHODS (Body Replacement)
            for method in cn.methods:
                if method.name.startsWith("<") or method.name.startsWith("$$mcp"):
                    continue
                
                if (method.access & Opcodes.ACC_ABSTRACT) or (method.access & Opcodes.ACC_NATIVE):
                    continue

                m_uid = str(uuid.uuid4())
                REGISTRY["methods"][m_uid] = {
                    "owner": original_owner,
                    "name": method.name,
                    "desc": method.desc
                }

                method.instructions.clear()
                method.tryCatchBlocks.clear()
                method.localVariables.clear()

                method.instructions.add(TypeInsnNode(Opcodes.NEW, "java/lang/Error"))
                method.instructions.add(InsnNode(Opcodes.DUP))
                method.instructions.add(LdcInsnNode(m_uid))
                method.instructions.add(MethodInsnNode(
                    Opcodes.INVOKESPECIAL, 
                    "java/lang/Error", 
                    "<init>", 
                    "(Ljava/lang/String;)V", 
                    False
                ))
                method.instructions.add(InsnNode(Opcodes.ATHROW))

            # Write Class
            cw = ClassWriter(ClassWriter.COMPUTE_MAXS)
            cn.accept(cw)
            zout.writestr(item.filename, cw.toByteArray())

# --- PHASE 2: EXTRACTION ---

def generate_tiny(remapped_jar_path, output_tiny_path):
    print(f"[*] Analyzing {remapped_jar_path} -> {output_tiny_path}")
    
    tiny_lines = ["v1\tofficial\tnamed"]
    classes = 0
    fields = 0
    methods = 0
    
    with zipfile.ZipFile(remapped_jar_path, 'r') as z:
        for filename in z.namelist():
            if not filename.endswith(".class"): continue
            
            bytes_in = z.read(filename)
            
            # FIX: Explicit cast here as well
            jbytes = JArray(JByte)(bytes_in)
            
            try:
                cr = ClassReader(jbytes)
                cn = ClassNode()
                cr.accept(cn, 0)
            except Exception as e:
                # If a class fails to parse, skip it
                print(f"Skipping {filename}: {e}")
                continue

            # 1. RESOLVE CLASSES
            c_uid = None
            for field in cn.fields:
                if field.name.endsWith("__MCP_UUID__"):
                    c_uid = field.value
                    break
            
            if not c_uid: continue

            
            orig_c_data = REGISTRY["classes"].get(c_uid)
            if not orig_c_data: continue

            original_c_name = orig_c_data["name"]
            mapped_c_name = cn.name
            classes+=1
            tiny_lines.append(f"CLASS\t{original_c_name}\t{mapped_c_name}")

            # 2. RESOLVE FIELDS
            for method in cn.methods:
                if method.name.contains("$$mcp_trace_"):

                    f_uid = str(method.name).split("$$mcp_trace_")[1]
                    
                    insn = method.instructions.getFirst()
                    while insn:
                        if isinstance(insn, FieldInsnNode):
                            mapped_f_name = insn.name
                            orig_f_data = REGISTRY["fields"].get(f_uid)
                            
                            if orig_f_data:
                                fields+=1
                                tiny_lines.append(
                                    f"FIELD\t{original_c_name}\t{orig_f_data['desc']}\t{orig_f_data['name']}\t{mapped_f_name}"
                                )
                            break
                        insn = insn.getNext()

            # 3. RESOLVE METHODS
            for method in cn.methods:
                insn = method.instructions.getFirst()
                while insn:
                    if isinstance(insn, LdcInsnNode):
                        m_uid = str(insn.cst)
                        if m_uid in REGISTRY["methods"]:
                            orig_m_data = REGISTRY["methods"][m_uid]
                            methods+=1
                            tiny_lines.append(
                                f"METHOD\t{original_c_name}\t{orig_m_data['desc']}\t{orig_m_data['name']}\t{method.name}"
                            )
                        break
                    insn = insn.getNext()

    with open(output_tiny_path, "w") as f:
        f.write("\n".join(tiny_lines))
    print(f"[*] Done. Tiny file written to {output_tiny_path} with {classes} classes, {methods} methods, and {fields} fields")

