# MCP_Archive

An archive most public MCP versions. Along with my attempt at translating them into the more modern fabric .TINY format.

Please note here, due to the legacy nature of these mappings, they lack the 'intermediary' mappings needed for loom, and such require more work to be useful (beyond just remapping jars)

In addition, MCP is under an extremely restrictive license. So use with caution!



Also see [MCP-Archive](https://github.com/Aizistral-Studios/MCP-Archive.git) by 
Aizistral Studios, with an extensive archive of MCP CSVs. 



## Notes:
* These are collected from the following sources:

1. **Complete MCP packs** sourced from various locations across the internet

2. **MCP configs extracted from old Forge versions**
   - These versions appear to be preserved only within Forge distributions
   - Typically pre-release, beta, or development builds
   - Do not include MCP build tools

3. **MCPBot/Forge generated configs**
   - Later Forge versions only ship with TSRG files; these are combined with MCPBot data
   - These can be considered as reliable as the first two sources

4. **The [Zffu/mappings](https://github.com/Zffu/mappings) repository**
   - Contains newer MCP versions, but their authenticity is questionable
   - In overlapping versions, differences exist compared to other MCP builds
   - **Example from 1.12 IntegratedServer class:**
     - MCP: `theWorldSettings` vs Zffu: `worldSettings`
     - MCP: `getShowArms` vs Zffu: `causesSuffocation`
   - However, it contains many otherwise lost versions

5. **Hybrid MCPBot/Zffu mappings**
   - Generated using verified MCPBot CSVs combined with Zffu TSRG files

----------------
| Finding State     |  MCP Version   |   Tiny V1    | Minecraft Version |
|-------------------|----------------|--------------|-------------------|
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.1.2/revengpack16.zip)) | revengpack16 | a1.1.2 | [a1.1.2-revengpack16.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.1.2/a1.1.2-revengpack16.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.1_01/mcp20a.zip)) | mcp20a | a1.2.1_01 | [a1.2.1_01-mcp20a.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.1_01/a1.2.1_01-mcp20a.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.1_01/mcp20.zip)) | mcp20 | a1.2.1_01 | [a1.2.1_01-mcp20.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.1_01/a1.2.1_01-mcp20.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.2/mcp21.zip)) | mcp21 | a1.2.2a | [a1.2.2a-mcp21.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.2/a1.2.2a-mcp21.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.2/mcp22.zip)) | mcp22 | a1.2.2a | [a1.2.2a-mcp22.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.2/a1.2.2a-mcp22.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.2/mcp22a.zip)) | mcp22a | a1.2.2a | [a1.2.2a-mcp22a.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.2/a1.2.2a-mcp22a.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.2/mcp21.zip)) | mcp21 | a1.2.2b | [a1.2.2b-mcp21.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.2/a1.2.2b-mcp21.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.2/mcp22.zip)) | mcp22 | a1.2.2b | [a1.2.2b-mcp22.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.2/a1.2.2b-mcp22.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.2/mcp22a.zip)) | mcp22a | a1.2.2b | [a1.2.2b-mcp22a.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.2/a1.2.2b-mcp22a.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.3_04/mcp23.zip)) | mcp23 | a1.2.3_02 | [a1.2.3_02-mcp23.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.3_04/a1.2.3_02-mcp23.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.5/mcp24.zip)) | mcp24 | a1.2.5 | [a1.2.5-mcp24.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.5/a1.2.5-mcp24.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/a1.2.6/mcp25.zip)) | mcp25 | a1.2.6 | [a1.2.6-mcp25.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/a1.2.6/a1.2.6-mcp25.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.1_02/mcp26.zip)) | mcp26 | b1.1_02 | [b1.1_02-mcp26.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.1_02/b1.1_02-mcp26.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.2_01/mcp27.zip)) | mcp27 | b1.2_01 | [b1.2_01-mcp27.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.2_01/b1.2_01-mcp27.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.2_01/mcp28.zip)) | mcp28 | b1.2_01 | [b1.2_01-mcp28.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.2_01/b1.2_01-mcp28.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.3_01/mcp29.zip)) | mcp29 | b1.3_01 | [b1.3_01-mcp29.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.3_01/b1.3_01-mcp29.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.3_01/mcp29a.zip)) | mcp29a | b1.3_01 | [b1.3_01-mcp29a.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.3_01/b1.3_01-mcp29a.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.4/mcp210.zip)) | mcp210 | b1.4 | [b1.4-mcp210.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.4/b1.4-mcp210.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.4_01/mcp30.zip)) | mcp30 | b1.4_01 | [b1.4_01-mcp30.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.4_01/b1.4_01-mcp30.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.4_01/mcp211.zip)) | mcp211 | b1.4_01 | [b1.4_01-mcp211.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.4_01/b1.4_01-mcp211.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.5._01/mcp31.zip)) | mcp31 | b1.5_01 | [b1.5_01-mcp31.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.5._01/b1.5_01-mcp31.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.5._01/mcp212.zip)) | mcp212 | b1.5_01 | [b1.5_01-mcp212.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.5._01/b1.5_01-mcp212.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.6.4/mcp32.zip)) | mcp32 | b1.6.4 | [b1.6.4-mcp32.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.6.4/b1.6.4-mcp32.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.6.5/mcp33.zip)) | mcp33 | b1.6.5 | [b1.6.5-mcp33.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.6.5/b1.6.5-mcp33.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.6.6/mcp34.zip)) | mcp34 | b1.6.6 | [b1.6.6-mcp34.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.6.6/b1.6.6-mcp34.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.6.6/mcp40.zip)) | mcp40 | b1.6.6 | [b1.6.6-mcp40.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.6.6/b1.6.6-mcp40.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.6.6/mcp41.zip)) | mcp41 | b1.6.6 | [b1.6.6-mcp41.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.6.6/b1.6.6-mcp41.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.7.2/mcp42.zip)) | mcp42 | b1.7.2 | [b1.7.2-mcp42.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.7.2/b1.7.2-mcp42.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.7.3/mcp43.zip)) | mcp43 | b1.7.3 | [b1.7.3-mcp43.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.7.3/b1.7.3-mcp43.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.8.1/mcp44.zip)) | mcp44 | b1.8.1 | [b1.8.1-mcp44.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.8.1/b1.8.1-mcp44.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/b1.9pre-5/mcp45pre.zip)) | mcp45pre | b1.9-pre5 | [@omni@b1.9-pre5-mcp45pre.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/b1.9pre-5/@omni@b1.9-pre5-mcp45pre.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.0.0/mcp50.zip)) | mcp50 | 1.0 | [1.0-mcp50.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.0.0/1.0-mcp50.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.1.0/mcp56.zip)) | mcp56 | 1.1 | [1.1-mcp56.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.1.0/1.1-mcp56.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/12w17a/mcp65.zip)) | mcp65 | 12w17a-1424 | [@omni@12w17a-1424-mcp65.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/12w17a/@omni@12w17a-1424-mcp65.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/12w26a/mcp615.zip)) | mcp615 | 12w26a | [@omni@12w26a-mcp615.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/12w26a/@omni@12w26a-mcp615.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.2.3/mcp60.zip)) | mcp60 | 1.2.3 | [1.2.3-mcp60.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.2.3/1.2.3-mcp60.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.2.4/mcp61.zip)) | mcp61 | 1.2.4 | [1.2.4-mcp61.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.2.4/1.2.4-mcp61.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.2.5/mcp62.zip)) | mcp62 | 1.2.5 | [1.2.5-mcp62.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.2.5/1.2.5-mcp62.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.3.1/mcp70a.zip)) | mcp70a | 1.3.1 | [1.3.1-mcp70a.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.3.1/1.3.1-mcp70a.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.3.1/mcp70.zip)) | mcp70 | 1.3.1 | [1.3.1-mcp70.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.3.1/1.3.1-mcp70.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.3.2/mcp72.zip)) | mcp72 | 1.3.2 | [1.3.2-mcp72.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.3.2/1.3.2-mcp72.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.4/mcp717_pre3.zip)) | mcp717_pre3 | 1.4 | [1.4-mcp717_pre3.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4/1.4-mcp717_pre3.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/1.4/mcp717)) | mcp717 | 1.4 | [1.4-mcp717.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4/1.4-mcp717.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/1.4.1/mcp718)) | mcp718 | 1.4.1 | [1.4.1-mcp718.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.1/1.4.1-mcp718.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.4.2/mcp719.zip)) | mcp719 | 1.4.2 | [1.4.2-mcp719.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.2/1.4.2-mcp719.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.4.3/mcp720pre1.zip)) | mcp720pre1 | 1.4.3 | [1.4.3-mcp720pre1.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.3/1.4.3-mcp720pre1.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/1.4.3/mcp720)) | mcp720 | 1.4.3 | [1.4.3-mcp720.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.3/1.4.3-mcp720.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.4.4/mcp721.zip)) | mcp721 | 1.4.4 | [1.4.4-mcp721.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.4/1.4.4-mcp721.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/1.4.5/mcp722)) | mcp722 | 1.4.5 | [1.4.5-mcp722.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.5/1.4.5-mcp722.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.4.5/mcp723.zip)) | mcp723 | 1.4.5 | [1.4.5-mcp723.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.5/1.4.5-mcp723.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.4.6/mcp725.zip)) | mcp725 | 1.4.6 | [1.4.6-mcp725.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.6/1.4.6-mcp725.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.4.7/mcp726.zip)) | mcp726 | 1.4.7 | [1.4.7-mcp726.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.7/1.4.7-mcp726.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.4.7/mcp726a.zip)) | mcp726a | 1.4.7 | [1.4.7-mcp726a.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.4.7/1.4.7-mcp726a.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/13w02b/mcp730)) | mcp730 | 13w02b | [@omni@13w02b-mcp730.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/@omni@13w02b/@omni@13w02b-mcp730.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/13w02b/mcp730c.zip)) | mcp730c | 13w02b | [@omni@13w02b-mcp730c.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/13w02b/@omni@13w02b-mcp730c.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/13w09c/mcp739.zip)) | mcp739 | 13w09c | [@omni@13w09c-mcp739.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/13w09c/@omni@13w09c-mcp739.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.5/mcp742.zip)) | mcp742 | 1.5 | [1.5-mcp742.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.5/1.5-mcp742.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.5.1/mcp744.zip)) | mcp744 | 1.5.1 | [1.5.1-mcp744.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.5.1/1.5.1-mcp744.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.5.2/mcp751.zip)) | mcp751 | 1.5.2 | [1.5.2-mcp751.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.5.2/1.5.2-mcp751.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/1.6/mcp801)) | mcp801 | 1.6 | [1.6-mcp801.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.6/1.6-mcp801.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.6/mcp801-pre.zip)) | mcp801-pre | 1.6.1 | [1.6.1-mcp801-pre.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.6/1.6.1-mcp801-pre.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.6.1/mcp802.zip)) | mcp802 | 1.6.1 | [1.6.1-mcp802.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.6.1/1.6.1-mcp802.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.6.1/mcp803.zip)) | mcp803 | 1.6.1 | [1.6.1-mcp803.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.6.1/1.6.1-mcp803.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.6.2/mcp804.zip)) | mcp804 | 1.6.2 | [1.6.2-mcp804.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.6.2/1.6.2-mcp804.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.6.2/mcp805.zip)) | mcp805 | 1.6.2 | [1.6.2-mcp805.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.6.2/1.6.2-mcp805.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.6.3/mcp809.zip)) | mcp809 | 1.6.3 | [1.6.3-mcp809.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.6.3/1.6.3-mcp809.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.6.4/mcp811.zip)) | mcp811 | 1.6.3 | [1.6.3-mcp811.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.6.4/1.6.3-mcp811.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/1.7.2/mcp901-alpha)) | mcp901-alpha | 1.7.2 | [1.7.2-mcp901-alpha.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.7.2/1.7.2-mcp901-alpha.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.7.2/mcp902beta.zip)) | mcp902beta | 1.7.2 | [1.7.2-mcp902beta.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.7.2/1.7.2-mcp902beta.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.7.2/mcp903.zip)) | mcp903 | 1.7.2 | [1.7.2-mcp903.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.7.2/1.7.2-mcp903.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/1.7.9/mcp904)) | mcp904 | 1.7.9 | [1.7.9-mcp904.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.7.9/1.7.9-mcp904.tiny) |
| 🟢 Early Forge Config ([link](https://github.com/GrylaMC/MCP_Archive/tree/main/extracted_forge_configs/1.7.10/mcp905)) | mcp905 | 1.7.10 | [1.7.10-mcp905.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.7.10/1.7.10-mcp905.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.7.10/mcp908.zip)) | mcp908 | 1.7.10 | [1.7.10-mcp908.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.7.10/1.7.10-mcp908.tiny) |
| 🟣 MCPBot/Zffu config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_zffu_mcpbot_configs/1.7.10/)) |  | 1.7.10 | [1.7.10-mcpbotZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.7.10/1.7.10-mcpbotZFFU.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.8/mcp910-pre1.zip)) | mcp910-pre1 | 1.8 | [1.8-mcp910-pre1.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.8/1.8-mcp910-pre1.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.8.8/mcp918.zip)) | mcp918 | 1.8.8 | [1.8.8-mcp918.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.8.8/1.8.8-mcp918.tiny) |
| 🟣 MCPBot/Zffu config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_zffu_mcpbot_configs/1.8.8/)) |  | 1.8.8 | [1.8.8-mcpbotZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.8.8/1.8.8-mcpbotZFFU.tiny) |
| 🟣 MCPBot/Zffu config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_zffu_mcpbot_configs/1.8.9/)) |  | 1.8.9 | [1.8.9-mcpbotZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.8.9/1.8.9-mcpbotZFFU.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.9/mcp924-beta1.zip)) | mcp924-beta1 | 1.9 | [1.9-mcp924-beta1.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.9/1.9-mcp924-beta1.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.9.4/mcp928.zip)) | mcp928 | 1.9.4 | [1.9.4-mcp928.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.9.4/1.9.4-mcp928.tiny) |
| 🟣 MCPBot/Zffu config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_zffu_mcpbot_configs/1.9.4/)) |  | 1.9.4 | [1.9.4-mcpbotZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.9.4/1.9.4-mcpbotZFFU.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.10/mcp931.zip)) | mcp931 | 1.10 | [1.10-mcp931.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.10/1.10-mcp931.tiny) |
| ⚠️ Zffu Config ([link](https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/1.10/)) |  | 1.10 | [1.10-mcpZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.10/1.10-mcpZFFU.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.11/mcp935-rc1.zip)) | mcp935-rc1 | 1.11 | [1.11-mcp935-rc1.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.11/1.11-mcp935-rc1.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.11.2/mcp937.zip)) | mcp937 | 1.11.2 | [1.11.2-mcp937.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.11.2/1.11.2-mcp937.tiny) |
| ⚠️ Zffu Config ([link](https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/1.11.2/)) |  | 1.11.2 | [1.11.2-mcpZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.11.2/1.11.2-mcpZFFU.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.12/mcp940.zip)) | mcp940 | 1.12 | [1.12-mcp940.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.12/1.12-mcp940.tiny) |
| 🟣 MCPBot/Zffu config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_zffu_mcpbot_configs/1.12/)) |  | 1.12 | [1.12-mcpbotZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.12/1.12-mcpbotZFFU.tiny) |
| ⭐ Found Completely ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/1.12.2/mcp942.zip)) | mcp942 | 1.12.2 | [1.12.2-mcp942.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.12.2/1.12.2-mcp942.tiny) |
| ⚠️ Zffu Config ([link](https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/1.12.2/)) |  | 1.12.2 | [1.12.2-mcpZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.12.2/1.12.2-mcpZFFU.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.13/)) |  | 1.13 | [1.13-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.13/1.13-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.13.1/)) |  | 1.13.1 | [1.13.1-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.13.1/1.13.1-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.13.2/)) |  | 1.13.2 | [1.13.2-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.13.2/1.13.2-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.14/)) |  | 1.14 | [1.14-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.14/1.14-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.14.1/)) |  | 1.14.1 | [1.14.1-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.14.1/1.14.1-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.14.2/)) |  | 1.14.2 | [1.14.2-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.14.2/1.14.2-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.14.3/)) |  | 1.14.3 | [1.14.3-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.14.3/1.14.3-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.14.4/)) |  | 1.14.4 | [1.14.4-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.14.4/1.14.4-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.15/)) |  | 1.15 | [1.15-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.15/1.15-mcpbotFORGE.tiny) |
| 🟣 MCPBot/Forge config ([link](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/generated_forge_mcpbot_configs/1.15.1/)) |  | 1.15.1 | [1.15.1-mcpbotFORGE.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.15.1/1.15.1-mcpbotFORGE.tiny) |
| ⚠️ Zffu Config ([link](https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/1.16/)) |  | 1.16 | [1.16-mcpZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.16/1.16-mcpZFFU.tiny) |
| ⚠️ Zffu Config ([link](https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/1.16.1/)) |  | 1.16.1 | [1.16.1-mcpZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.16.1/1.16.1-mcpZFFU.tiny) |
| ⚠️ Zffu Config ([link](https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/1.16.2/)) |  | 1.16.2 | [1.16.2-mcpZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.16.2/1.16.2-mcpZFFU.tiny) |
| ⚠️ Zffu Config ([link](https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/1.16.3/)) |  | 1.16.3 | [1.16.3-mcpZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.16.3/1.16.3-mcpZFFU.tiny) |
| ⚠️ Zffu Config ([link](https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/1.16.4/)) |  | 1.16.4 | [1.16.4-mcpZFFU.tiny](https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/1.16.4/1.16.4-mcpZFFU.tiny) |
