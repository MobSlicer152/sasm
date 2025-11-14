; comment

; label
add:
    ; make a new stack frame
    push ebp
    mov ebp, esp

    ; this is 32-bit, can just use cdecl
    ; return address and arguments are above ebp
    mov eax, DWORD PTR [ebp + 8] ; get first argument
    add eax, DWORD PTR [ebp + 12] ; add second argument

    ; clean up stack frame, eax is the return value
    pop ebp
    ret
