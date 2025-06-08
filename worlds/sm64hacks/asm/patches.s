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
    BNE T2, T3, _end
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
    B _return
    NOP
_return:
    LW RA, 0x0014(SP)
    ADDIU SP, SP, 0x28
    JR RA
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