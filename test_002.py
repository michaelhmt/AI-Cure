import pymem
import pymem.process

# Attach to the process
pm = pymem.Pymem('YourGame.exe')

# Allocate memory in the target process
allocated_address = pymem.process.allocate(pm.process_handle, size=1024)  # Allocate 1024 bytes

# Your shellcode or assembly code as bytes
# For example, NOP (0x90) instruction - usually, you'd place your own assembly code here
shellcode = r"""
// ORIGINAL CODE - INJECTION POINT: oc_CScriptList

HoloCure.exe.text+223103B: 48 8B 05 16 8F 12 01     - mov rax,[gml_CScriptList]
HoloCure.exe.text+2231042: 48 83 3C 03 00           - cmp qword ptr [rbx+rax],00
HoloCure.exe.text+2231047: 74 31                    - je HoloCure.exe.text+223107A
HoloCure.exe.text+2231049: 48 8B 05 F0 8E 12 01     - mov rax,[HoloCure.exe+335AF40]
HoloCure.exe.text+2231050: 48 8D 0D 51 1E 5F 00     - lea rcx,[HoloCure.exe.rdata+59EA8]
HoloCure.exe.text+2231057: 41 B8 0B 00 00 00        - mov r8d,0000000B
HoloCure.exe.text+223105D: 48 8B 1C 03              - mov rbx,[rbx+rax]
HoloCure.exe.text+2231061: 48 8B D3                 - mov rdx,rbx
HoloCure.exe.text+2231064: E8 37 A0 1F 00           - call HoloCure.exe.text+242B0A0
HoloCure.exe.text+2231069: 85 C0                    - test eax,eax
HoloCure.exe.text+223106B: 75 04                    - jne HoloCure.exe.text+2231071
HoloCure.exe.text+223106D: 48 83 C3 0B              - add rbx,0B
HoloCure.exe.text+2231071: 48 8B C3                 - mov rax,rbx
HoloCure.exe.text+2231074: 48 83 C4 20              - add rsp,20
HoloCure.exe.text+2231078: 5B                       - pop rbx
HoloCure.exe.text+2231079: C3                       - ret
HoloCure.exe.text+223107A: 48 8D 05 9F 9E 66 00     - lea rax,[HoloCure.exe.rdata+D1F20]
HoloCure.exe.text+2231081: 48 83 C4 20              - add rsp,20
HoloCure.exe.text+2231085: 5B                       - pop rbx
HoloCure.exe.text+2231086: C3                       - ret
HoloCure.exe.text+2231087: CC                       - int 3
HoloCure.exe.text+2231088: CC                       - int 3
HoloCure.exe.text+2231089: CC                       - int 3
HoloCure.exe.text+223108A: CC                       - int 3
HoloCure.exe.text+223108B: CC                       - int 3
HoloCure.exe.text+223108C: CC                       - int 3
HoloCure.exe.text+223108D: CC                       - int 3
HoloCure.exe.text+223108E: CC                       - int 3
HoloCure.exe.text+223108F: CC                       - int 3
HoloCure.exe.text+2231090: 48 83 EC 28              - sub rsp,28
// ---------- INJECTING HERE ----------
oc_CScriptList: 48 83 3D BC 8E 12 01 00  - cmp qword ptr [gml_CScriptList],00
// ---------- DONE INJECTING  ----------
HoloCure.exe.text+223109C: 0F 84 C6 00 00 00        - je HoloCure.exe.text+2231168
HoloCure.exe.text+22310A2: 48 8B 0D 77 5C D9 00     - mov rcx,[HoloCure.exe.data+D20]
HoloCure.exe.text+22310A9: 48 8D 15 18 78 67 00     - lea rdx,[HoloCure.exe.rdata+DF8C8] (Script_Init called with Script_Main_number %d)
HoloCure.exe.text+22310B0: 44 8B 05 91 8E 12 01     - mov r8d,[HoloCure.exe+335AF48]
HoloCure.exe.text+22310B7: 48 89 74 24 38           - mov [rsp+38],rsi
HoloCure.exe.text+22310BC: 48 89 7C 24 20           - mov [rsp+20],rdi
HoloCure.exe.text+22310C1: 48 8B 01                 - mov rax,[rcx]
HoloCure.exe.text+22310C4: FF 50 10                 - call qword ptr [rax+10]
HoloCure.exe.text+22310C7: 33 F6                    - xor esi,esi
HoloCure.exe.text+22310C9: 83 3D 78 8E 12 01 01     - cmp dword ptr [HoloCure.exe+335AF48],01
HoloCure.exe.text+22310D0: 8B FE                    - mov edi,esi
HoloCure.exe.text+22310D2: 78 58                    - js HoloCure.exe.text+223112C
HoloCure.exe.text+22310D4: 48 89 5C 24 30           - mov [rsp+30],rbx
HoloCure.exe.text+22310D9: 8B DE                    - mov ebx,esi
HoloCure.exe.text+22310DB: 0F 1F 44 00 00           - nop dword ptr [rax+rax+00]
HoloCure.exe.text+22310E0: 48 8B 05 71 8E 12 01     - mov rax,[gml_CScriptList]
HoloCure.exe.text+22310E7: 48 8B 0C 03              - mov rcx,[rbx+rax]
HoloCure.exe.text+22310EB: 48 85 C9                 - test rcx,rcx
HoloCure.exe.text+22310EE: 74 25                    - je HoloCure.exe.text+2231115
HoloCure.exe.text+22310F0: E8 5B FA FF FF           - call HoloCure.exe.text+2230B50
HoloCure.exe.text+22310F5: 48 8B 05 44 8E 12 01     - mov rax,[HoloCure.exe+335AF40]
HoloCure.exe.text+22310FC: 48 8B 0C 03              - mov rcx,[rbx+rax]
HoloCure.exe.text+2231100: 48 85 C9                 - test rcx,rcx
HoloCure.exe.text+2231103: 74 10                    - je HoloCure.exe.text+2231115
HoloCure.exe.text+2231105: E8 B6 DB F1 FF           - call HoloCure.exe.text+214ECC0
HoloCure.exe.text+223110A: 48 8B 05 2F 8E 12 01     - mov rax,[HoloCure.exe+335AF40]
HoloCure.exe.text+2231111: 48 89 34 03              - mov [rbx+rax],rsi
HoloCure.exe.text+2231115: 8B 05 2D 8E 12 01        - mov eax,[HoloCure.exe+335AF48]
HoloCure.exe.text+223111B: FF C7                    - inc edi
HoloCure.exe.text+223111D: 48 83 C3 08              - add rbx,08
}
{
// ORIGINAL CODE - INJECTION POINT: oc_ObjectArray

HoloCure.exe.text+220FEBB: 0F 1F 44 00 00                 - nop dword ptr [rax+rax+00]
HoloCure.exe.text+220FEC0: 66 41 0F 6E 44 14 08           - movd xmm0,[r12+rdx+08]
HoloCure.exe.text+220FEC7: 4C 8D 0D CA 75 69 00           - lea r9,[HoloCure.exe.rdata+DE498] (sequence event)
HoloCure.exe.text+220FECE: 49 8B 85 A0 00 00 00           - mov rax,[r13+000000A0]
HoloCure.exe.text+220FED5: 48 8D 15 CC 75 69 00           - lea rdx,[HoloCure.exe.rdata+DE4A8] (event_type)
HoloCure.exe.text+220FEDC: F3 0F E6 C0                    - cvtdq2pd xmm0,xmm0
HoloCure.exe.text+220FEE0: B9 03 00 00 00                 - mov ecx,00000003
HoloCure.exe.text+220FEE5: 49 8B 04 07                    - mov rax,[r15+rax]
HoloCure.exe.text+220FEE9: 48 89 44 24 48                 - mov [rsp+48],rax
HoloCure.exe.text+220FEEE: F2 0F 11 74 24 40              - movsd [rsp+40],xmm6
HoloCure.exe.text+220FEF4: 0F 28 D6                       - movaps xmm2,xmm6
HoloCure.exe.text+220FEF7: 48 89 5C 24 38                 - mov [rsp+38],rbx
HoloCure.exe.text+220FEFC: 66 49 0F 7E F0                 - movq r8,xmm6
HoloCure.exe.text+220FF01: 48 C7 44 24 30 00 00 00 00     - mov qword ptr [rsp+30],00000000
HoloCure.exe.text+220FF0A: F2 0F 11 44 24 28              - movsd [rsp+28],xmm0
HoloCure.exe.text+220FF10: 48 89 7C 24 20                 - mov [rsp+20],rdi
HoloCure.exe.text+220FF15: E8 B6 30 F4 FF                 - call HoloCure.exe.text+2152FD0
HoloCure.exe.text+220FF1A: 48 8B 15 7F 83 14 01           - mov rdx,[HoloCure.exe+33592A0]
HoloCure.exe.text+220FF21: 48 8D 0D F8 6B DB 00           - lea rcx,[HoloCure.exe.data+B20]
HoloCure.exe.text+220FF28: 41 B9 4C 00 00 00              - mov r9d,0000004C
HoloCure.exe.text+220FF2E: 89 05 58 B6 DB 00              - mov [HoloCure.exe.data+558C],eax
HoloCure.exe.text+220FF34: 45 8D 41 BB                    - lea r8d,[r9-45]
HoloCure.exe.text+220FF38: E8 23 F9 FF FF                 - call HoloCure.exe.text+220F860
HoloCure.exe.text+220FF3D: 48 8B 3D 94 1C F2 00           - mov rdi,[HoloCure.exe.data+16BBD8]
HoloCure.exe.text+220FF44: 33 F6                          - xor esi,esi
HoloCure.exe.text+220FF46: 48 63 2D 53 34 17 01           - movsxd  rbp,dword ptr [HoloCure.exe+33843A0]
HoloCure.exe.text+220FF4D: 48 8D 47 01                    - lea rax,[rdi+01]
HoloCure.exe.text+220FF51: 48 89 05 80 1C F2 00           - mov [HoloCure.exe.data+16BBD8],rax
HoloCure.exe.text+220FF58: 48 85 ED                       - test rbp,rbp
HoloCure.exe.text+220FF5B: 0F 8E AF 00 00 00              - jng HoloCure.exe.text+2210010
// ---------- INJECTING HERE ----------
oc_ObjectArray: 4C 8B 0D 38 52 F3 00           - mov r9,[gml_ObjectArray]
// ---------- DONE INJECTING  ----------
HoloCure.exe.text+220FF68: 0F 1F 84 00 00 00 00 00        - nop dword ptr [rax+rax+00000000]
HoloCure.exe.text+220FF70: 48 8B 05 C1 9B 16 01           - mov rax,[HoloCure.exe+337AB38]
HoloCure.exe.text+220FF77: 49 63 49 08                    - movsxd  rcx,dword ptr [r9+08]
HoloCure.exe.text+220FF7B: 4C 63 04 B0                    - movsxd  r8,dword ptr [rax+rsi*4]
HoloCure.exe.text+220FF7F: 49 8B 01                       - mov rax,[r9]
HoloCure.exe.text+220FF82: 49 23 C8                       - and rcx,r8
HoloCure.exe.text+220FF85: 48 03 C9                       - add rcx,rcx
HoloCure.exe.text+220FF88: 48 8B 14 C8                    - mov rdx,[rax+rcx*8]
HoloCure.exe.text+220FF8C: 48 85 D2                       - test rdx,rdx
HoloCure.exe.text+220FF8F: 74 73                          - je HoloCure.exe.text+2210004
HoloCure.exe.text+220FF91: 44 39 42 10                    - cmp [rdx+10],r8d
HoloCure.exe.text+220FF95: 74 1F                          - je HoloCure.exe.text+220FFB6
HoloCure.exe.text+220FF97: 48 8B 52 08                    - mov rdx,[rdx+08]
HoloCure.exe.text+220FF9B: 48 85 D2                       - test rdx,rdx
HoloCure.exe.text+220FF9E: 75 F1                          - jne HoloCure.exe.text+220FF91
HoloCure.exe.text+220FFA0: EB 62                          - jmp HoloCure.exe.text+2210004
HoloCure.exe.text+220FFA2: 8B 84 24 A8 00 00 00           - mov eax,[rsp+000000A8]
HoloCure.exe.text+220FFA9: 48 8B 94 24 B0 00 00 00        - mov rdx,[rsp+000000B0]
HoloCure.exe.text+220FFB1: E9 EF FE FF FF                 - jmp HoloCure.exe.text+220FEA5
HoloCure.exe.text+220FFB6: 48 8B 5A 18                    - mov rbx,[rdx+18]
HoloCure.exe.text+220FFBA: 48 85 DB                       - test rbx,rbx
HoloCure.exe.text+220FFBD: 74 45                          - je HoloCure.exe.text+2210004
HoloCure.exe.text+220FFBF: 48 8B 5B 50                    - mov rbx,[rbx+50]
HoloCure.exe.text+220FFC3: 48 85 DB                       - test rbx,rbx
HoloCure.exe.text+220FFC6: 74 35                          - je HoloCure.exe.text+220FFFD
HoloCure.exe.text+220FFC8: 48 8B 4B 10                    - mov rcx,[rbx+10]
HoloCure.exe.text+220FFCC: 48 85 C9                       - test rcx,rcx
HoloCure.exe.text+220FFCF: 74 2C                          - je HoloCure.exe.text+220FFFD
HoloCure.exe.text+220FFD1: F7 81 B0 00 00 00 03 00 10 00  - test [rcx+000000B0],00100003
HoloCure.exe.text+220FFDB: 48 8B 1B                       - mov rbx,[rbx]
}
{
// ORIGINAL CODE - INJECTION POINT: oc_GlobalVariables

HoloCure.exe.text+21687C4: 0F 29 74 24 60           - movaps [rsp+60],xmm6
HoloCure.exe.text+21687C9: 48 8B 05 A8 70 EC 00     - mov rax,[HoloCure.exe.data+69878]
HoloCure.exe.text+21687D0: 48 33 C4                 - xor rax,rsp
HoloCure.exe.text+21687D3: 48 89 44 24 50           - mov [rsp+50],rax
HoloCure.exe.text+21687D8: 8B DA                    - mov ebx,edx
HoloCure.exe.text+21687DA: 89 54 24 34              - mov [rsp+34],edx
HoloCure.exe.text+21687DE: 4C 8B F1                 - mov r14,rcx
HoloCure.exe.text+21687E1: 48 89 4C 24 38           - mov [rsp+38],rcx
HoloCure.exe.text+21687E6: 48 8B 0D C3 2D E6 00     - mov rcx,[HoloCure.exe.data+55B0]
HoloCure.exe.text+21687ED: 48 8B 01                 - mov rax,[rcx]
HoloCure.exe.text+21687F0: 44 8B CA                 - mov r9d,edx
HoloCure.exe.text+21687F3: 4D 8B C6                 - mov r8,r14
HoloCure.exe.text+21687F6: 48 8D 15 6B E3 6B 00     - lea rdx,[HoloCure.exe.rdata+5DB68] (initialise everything! %p, %u)
HoloCure.exe.text+21687FD: FF 50 10                 - call qword ptr [rax+10]
HoloCure.exe.text+2168800: E8 4B 7A 07 00           - call HoloCure.exe.text+21E0250
HoloCure.exe.text+2168805: E8 D6 C5 0E 00           - call HoloCure.exe.text+2254DE0
HoloCure.exe.text+216880A: E8 31 1F 05 00           - call HoloCure.exe.text+21BA740
HoloCure.exe.text+216880F: E8 7C 88 0C 00           - call HoloCure.exe.text+2231090
HoloCure.exe.text+2168814: E8 97 C0 0F 00           - call HoloCure.exe.text+22648B0
HoloCure.exe.text+2168819: E8 82 3F 0B 00           - call HoloCure.exe.text+221C7A0
HoloCure.exe.text+216881E: E8 5D BA 04 00           - call HoloCure.exe.text+21B4280
HoloCure.exe.text+2168823: E8 E8 52 10 00           - call HoloCure.exe.text+226DB10
HoloCure.exe.text+2168828: E8 D3 57 10 00           - call HoloCure.exe.text+226E000
HoloCure.exe.text+216882D: 80 3D 0C FB 1E 01 00     - cmp byte ptr [HoloCure.exe+3359340],00
HoloCure.exe.text+2168834: 74 11                    - je HoloCure.exe.text+2168847
HoloCure.exe.text+2168836: 48 8D 0D EB 17 1F 01     - lea rcx,[HoloCure.exe+335B028]
HoloCure.exe.text+216883D: E8 3E EC 0D 00           - call HoloCure.exe.text+2247480
HoloCure.exe.text+2168842: E8 E9 F5 11 00           - call HoloCure.exe.text+2287E30
HoloCure.exe.text+2168847: 48 8B 15 E2 3C FD 00     - mov rdx,[HoloCure.exe+313D530]
HoloCure.exe.text+216884E: 8B 0D D4 3C FD 00        - mov ecx,[HoloCure.exe+313D528]
// ---------- INJECTING HERE ----------
oc_GlobalVariables: 48 83 3D BC 3C FD 00 00  - cmp qword ptr [gml_GlobalVariables],00
// ---------- DONE INJECTING  ----------
HoloCure.exe.text+216885C: 75 17                    - jne HoloCure.exe.text+2168875
HoloCure.exe.text+216885E: 48 85 D2                 - test rdx,rdx
HoloCure.exe.text+2168861: 0F 84 6C 01 00 00        - je HoloCure.exe.text+21689D3
HoloCure.exe.text+2168867: 8B 42 0C                 - mov eax,[rdx+0C]
HoloCure.exe.text+216886A: 85 C0                    - test eax,eax
HoloCure.exe.text+216886C: 0F 4F C8                 - cmovg ecx,eax
HoloCure.exe.text+216886F: 89 0D B3 3C FD 00        - mov [HoloCure.exe+313D528],ecx
HoloCure.exe.text+2168875: 48 85 D2                 - test rdx,rdx
HoloCure.exe.text+2168878: 0F 84 55 01 00 00        - je HoloCure.exe.text+21689D3
HoloCure.exe.text+216887E: 8B 42 10                 - mov eax,[rdx+10]
HoloCure.exe.text+2168881: 8B 15 A5 3C FD 00        - mov edx,[HoloCure.exe+313D52C]
HoloCure.exe.text+2168887: 85 C0                    - test eax,eax
HoloCure.exe.text+2168889: 0F 4F D0                 - cmovg edx,eax
HoloCure.exe.text+216888C: 89 15 9A 3C FD 00        - mov [HoloCure.exe+313D52C],edx
HoloCure.exe.text+2168892: 45 33 C0                 - xor r8d,r8d
HoloCure.exe.text+2168895: E8 66 15 05 00           - call HoloCure.exe.text+21B9E00
HoloCure.exe.text+216889A: 48 8B 05 8F 3C FD 00     - mov rax,[HoloCure.exe+313D530]
HoloCure.exe.text+21688A1: 48 8B 78 18              - mov rdi,[rax+18]
HoloCure.exe.text+21688A5: 33 ED                    - xor ebp,ebp
HoloCure.exe.text+21688A7: 8B 0D 7B 3C FD 00        - mov ecx,[HoloCure.exe+313D528]
HoloCure.exe.text+21688AD: 85 C9                    - test ecx,ecx
HoloCure.exe.text+21688AF: 0F 8E 1E 01 00 00        - jng HoloCure.exe.text+21689D3
HoloCure.exe.text+21688B5: 48 8B 0F                 - mov rcx,[rdi]
HoloCure.exe.text+21688B8: 48 8B 09                 - mov rcx,[rcx]
HoloCure.exe.text+21688BB: E8 F0 E3 FD FF           - call HoloCure.exe.text+2146CB0
HoloCure.exe.text+21688C0: 48 8B F0                 - mov rsi,rax
HoloCure.exe.text+21688C3: BA 01 00 00 00           - mov edx,00000001
HoloCure.exe.text+21688C8: 44 8B C2                 - mov r8d,edx
HoloCure.exe.text+21688CB: 48 8B C8                 - mov rcx,rax
HoloCure.exe.text+21688CE: E8 9D 13 05 00           - call HoloCure.exe.text+21B9C70
}
{
// ORIGINAL CODE - INJECTION POINT: oc_StringsList

HoloCure.exe.text+27DA50: 4D 8B C2                 - mov r8,r10
HoloCure.exe.text+27DA53: 48 FF C2                 - inc rdx
HoloCure.exe.text+27DA56: 49 83 C2 18              - add r10,18
HoloCure.exe.text+27DA5A: 41 8B 40 10              - mov eax,[r8+10]
HoloCure.exe.text+27DA5E: 85 C0                    - test eax,eax
HoloCure.exe.text+27DA60: 74 09                    - je HoloCure.exe.text+27DA6B
HoloCure.exe.text+27DA62: 78 07                    - js HoloCure.exe.text+27DA6B
HoloCure.exe.text+27DA64: 41 3B C9                 - cmp ecx,r9d
HoloCure.exe.text+27DA67: 74 09                    - je HoloCure.exe.text+27DA72
HoloCure.exe.text+27DA69: FF C1                    - inc ecx
HoloCure.exe.text+27DA6B: 49 3B D3                 - cmp rdx,r11
HoloCure.exe.text+27DA6E: 7C E0                    - jl HoloCure.exe.text+27DA50
HoloCure.exe.text+27DA70: EB 09                    - jmp HoloCure.exe.text+27DA7B
HoloCure.exe.text+27DA72: 49 8B 40 08              - mov rax,[r8+08]
HoloCure.exe.text+27DA76: 41 39 38                 - cmp [r8],edi
HoloCure.exe.text+27DA79: 74 08                    - je HoloCure.exe.text+27DA83
HoloCure.exe.text+27DA7B: 41 83 E9 01              - sub r9d,01
HoloCure.exe.text+27DA7F: 79 A4                    - jns HoloCure.exe.text+27DA25
HoloCure.exe.text+27DA81: EB 03                    - jmp HoloCure.exe.text+27DA86
HoloCure.exe.text+27DA83: 48 8B F0                 - mov rsi,rax
HoloCure.exe.text+27DA86: 4C 8B 34 24              - mov r14,[rsp]
HoloCure.exe.text+27DA8A: 48 8B C6                 - mov rax,rsi
HoloCure.exe.text+27DA8D: 48 8B 74 24 20           - mov rsi,[rsp+20]
HoloCure.exe.text+27DA92: 48 8B 6C 24 18           - mov rbp,[rsp+18]
HoloCure.exe.text+27DA97: 48 8B 5C 24 10           - mov rbx,[rsp+10]
HoloCure.exe.text+27DA9C: 48 8B 7C 24 28           - mov rdi,[rsp+28]
HoloCure.exe.text+27DAA1: 48 83 C4 08              - add rsp,08
HoloCure.exe.text+27DAA5: C3                       - ret
HoloCure.exe.text+27DAA6: 3B 3D 94 4E 55 00        - cmp edi,[HoloCure.exe.data+68940]
HoloCure.exe.text+27DAAC: 7D 29                    - jnl HoloCure.exe.text+27DAD7
// ---------- INJECTING HERE ----------
oc_StringsList: 48 8B 05 9B 4E 55 00     - mov rax,[HoloCure.exe.data+68950]
// ---------- DONE INJECTING  ----------
HoloCure.exe.text+27DAB5: 48 8B 74 24 20           - mov rsi,[rsp+20]
HoloCure.exe.text+27DABA: 48 8B 7C 24 28           - mov rdi,[rsp+28]
HoloCure.exe.text+27DABF: 48 63 CA                 - movsxd  rcx,edx
HoloCure.exe.text+27DAC2: 48 8B 9C C8 00 CB F3 FF  - mov rbx,[rax+rcx*8-000C3500]
HoloCure.exe.text+27DACA: 48 8B C3                 - mov rax,rbx
HoloCure.exe.text+27DACD: 48 8B 5C 24 10           - mov rbx,[rsp+10]
HoloCure.exe.text+27DAD2: 48 83 C4 08              - add rsp,08
HoloCure.exe.text+27DAD6: C3                       - ret
HoloCure.exe.text+27DAD7: 48 8B 74 24 20           - mov rsi,[rsp+20]
HoloCure.exe.text+27DADC: 33 DB                    - xor ebx,ebx
HoloCure.exe.text+27DADE: 48 8B 7C 24 28           - mov rdi,[rsp+28]
HoloCure.exe.text+27DAE3: 8B C3                    - mov eax,ebx
HoloCure.exe.text+27DAE5: 48 8B 5C 24 10           - mov rbx,[rsp+10]
HoloCure.exe.text+27DAEA: 48 83 C4 08              - add rsp,08
HoloCure.exe.text+27DAEE: C3                       - ret
HoloCure.exe.text+27DAEF: 85 D2                    - test edx,edx
HoloCure.exe.text+27DAF1: 78 1F                    - js HoloCure.exe.text+27DB12
HoloCure.exe.text+27DAF3: 3B 15 E7 A9 55 00        - cmp edx,[1407D94E0]
HoloCure.exe.text+27DAF9: 7D 17                    - jnl HoloCure.exe.text+27DB12
HoloCure.exe.text+27DAFB: 48 63 C2                 - movsxd  rax,edx
HoloCure.exe.text+27DAFE: 48 8D 0D EB A9 55 00     - lea rcx,[1407D94F0]
HoloCure.exe.text+27DB05: 48 C1 E0 05              - shl rax,05
HoloCure.exe.text+27DB09: 48 8B 04 08              - mov rax,[rax+rcx]
HoloCure.exe.text+27DB0D: 48 83 C4 08              - add rsp,08
HoloCure.exe.text+27DB11: C3                       - ret
HoloCure.exe.text+27DB12: 48 8D 05 27 18 3F 00     - lea rax,[HoloCure.exe.rdata+C4340] (&lt;unknown built-in variable&gt;)
HoloCure.exe.text+27DB19: 48 83 C4 08              - add rsp,08
HoloCure.exe.text+27DB1D: C3                       - ret
HoloCure.exe.text+27DB1E: CC                       - int 3
HoloCure.exe.text+27DB1F: CC                       - int 3
"""

# Write the shellcode to the allocated memory
pm.write_bytes(allocated_address, shellcode, len(shellcode))