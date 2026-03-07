.n64
.create "trap_patch", 0x8029D4B8
_start_trap:
    LA T1, _flag
    LW T2, 0(T1)
    ADDIU T3, R0, 0x0069
    BNE T2, T3, _heaveho
    NOP
    SW R0, 0(T1)
    LI A0, 0x80361158;mario
    LW A0, 0(A0)
    ADDIU A1, R0, 0x00D4 ;1-up model
    LI A2, 0x13004148 ;1-up bhv
    JAL 0x8029EDCC;spawn_object
    NOP
    LA T1, _greendemon
    SW V0, 0(T1);put pos of object in the greendemon memory address
    B _end
    NOP
_heaveho:;jump table would probably be better but i cba to do that
    ADDIU T3, T3, 0x0001
    BNE T2, T3, _spin
    NOP
    SW R0, 0(T1)
    LI A0, 0x80361158;mario
    LW A0, 0(A0)
    ADDIU A1, R0, 0x007A ;star model. heaveho model doesnt always exist so this is a good patchwork solution to that problem
    LI A2, 0x13001548 ;1-up bhv
    JAL 0x8029EDCC;spawn_object
    NOP
    LA T1, _heavehoaddr
    SW V0, 0(T1)
    B _end
    NOP
_spin:
    LA T1, _spinaddr
    LW T2, 0(T1)
    BNE T2, T3, _steve
    NOP
    LUI T4, 0x8034
    LHU T5, 0xC74C(T4)
    ADDIU T5, 0x50
    SH T5, 0xC74C(T4)
    B _end
    NOP
_steve:
    ADDIU T3, T3, 0x0001
    BNE T2, T3, _end
    NOP
    LA A2, 0x801F1000
    ADDIU A0, R0, 0x50
    JAL 0x802D6554 ;print_text
    ADDIU A1, R0, 0x50
    

;_choir:
 ;   LA T1, _choirflag
 ;   LW T2, 0(T1)
 ;   BEQ T2, R0, _undo
  ;  LUI T0, 0x2412 ;ADDU S2, R0, X
  ;  ADDU T0, T0, T2
  ;  LUI T3, 0x8032
 ;   B _end
 ;   SW T0, 0x91E0(T3) ;self-modifying code won't ever bite me in the ass...


    ;this is a janky solution as im changing the bank in a completely unrelated section of code but its the best i can do right now
    ;reloading song
    ;LUI T3, 0x8033
    ;LW T3, 0xDDCC(T3)
    ;OR A2, R0, R0
    ;LHU A0, 0x0036(T3)
    ;JAL 0x80249178;set_background_music
    ;LHU A1, 0x0038(T3)
;_undo:
 ;   LI T0, 0x8FD20048 ;LW S2, 0x0048
 ;   LUI T3, 0x8032
 ;   SW T0, 0x91E0(T3) ;self-modifying code won't ever bite me in the ass...
_end:
    B _return_traps
    NOP
_return_traps:
    LW RA, 0x0014(SP)
    ADDIU SP, SP, 0x28
    JR RA
    NOP
_spinaddr:
    NOP
_staraddr:
    NOP
_flag:
    NOP
_greendemon:
    NOP
_heavehoaddr:
    NOP
.close


.create "choir_patch", 0x8027FF00; this is to get "extra space" in load_banks_immediate to set s2 to the specific value we want
_start_choir:                    ; plenty of conventions are broken here in this "function" to save on space because of that
    LA T2, _choiraddr
    LW T2, 0(T2)
    BEQZ T2, _normal
    NOP
    B _end_choir
    ADDU S2, R0, T2
_normal:
    LW S2, 0x0048(FP)
_end_choir:
    JR RA
    NOP
_choiraddr:
    NOP
.close

.create "star_patch", 0x80279C88
_star:
   LA T3, _staraddr
   SW A1, 0(T3)
.close

.create "move_patch_hook", 0x802530B8 ; hook in set_jumping_action to extend function to the below code 
    J 0x8029AD80
    NOP
.close

.create "move_patch", 0x8029AD80 ;like above conventions are broken because i do NOT have the space in the parent function to not break them
_start_move_checks:
    LUI T7, 0x0000
    LI T9, 0x03000881
    BEQ T9, A1, _check_if_allowed ;double jump
    ORI T7, R0, 0x0002
    LI T9, 0x01000882
    BEQ T9, A1, _check_if_allowed ;triple jump
    ORI T7, R0, 0x0004
    LI T9, 0x03000888
    BEQ T9, A1, _check_if_allowed ;long jump
    ORI T7, R0, 0x0008
    LI T9, 0x01000883
    BEQ T9, A1, _check_if_allowed ;backflip
    ORI T7, R0, 0x0010
    LI T9, 0x01000887
    BEQ T9, A1, _check_if_allowed ;sideflip
    ORI T7, R0, 0x0020
    LI T9, 0x010008A6
    BEQ T9, A1, _go_back ;rollout, always allowed
    ORI T7, R0, 0x0001
_check_if_allowed:
    LA T9, _jumps_allowed
    LW T9, 0(T9)
    AND T7, T7, T9
    BEQZ T7, _return_moves
    NOP 
_go_back:
    J 0x802530C0
    NOP
_return_moves:
    OR V0, R0, R0
    ADDIU SP, SP, 0x20
    JR RA
    NOP
_jumps_allowed: ;single jump = 0x01, double jump = 0x02, triple jump = 0x04, long_jump = 0x08, backflip = 0x10, sideflip = 0x20
    NOP
.close


.create "decades_later_patch", 0x801E1000
    ADDIU T9, RA, 0x0000 ;BAD but i dont want to mess with SP in this "not a function"
    LW A0, 0x8032DDF4 ;gCurrSaveFileNum
    SRL A0, A0, 16
    JAL 0x8027A1C8 ;save_file_get_star_flags
    ADDIU A0, A0, -0x1
    ANDI V0, V0, 0x001F ;dont want to somehow accidentally end up on "act 7/8"
    ADDIU T7, V0, 0x0000
    LUI V0, 0x0000
_most_significant_bit:
    ADDIU V0, V0, 0x1
    ANDI T8, T7, 0x1
    SRL T7, T7, 0x1
    BNEZ T8, _most_significant_bit
    NOP
    LUI AT, 0x8034
    J 0x801D0A68
    ADDIU RA, T9, 0x0000
    NOP
.close



; set_mario_action deets:
; A0: mariostate
; A1: action id 

;i tried okay this just doesnt work for god knows what reason. it should work it just doesnt and fuck this

;.create "punch_or_kick_function", 0x8029AD80
;_punch_or_kick:
;    ADDIU SP, SP, -0x20
;    SW RA, 0x0014(SP)
;    SW A0, 0x0020(SP)
;    LW T6, 0x0020(SP)
;    LHU T7, 0x0002(T6)
;    ANDI T5, T7, 0x0080
;    BNEZ T5, _kick
;    NOP
;    LI A1, 0x00800380
;    JAL 0x80252CF4
;    OR A2, R0, R0
;    B _end
;    NOP
;_kick:
;    LI A1, 0x018008AC
;    JAL 0x80252CF4
;    OR A2, R0, R0
;_end:
;    LW RA, 0x0014(SP)
;    ADDIU SP, SP, 0x20
;    JR RA
;    NOP
;.close
