10 REM A BASIC PROGRAM THAT CAN BE USED FOR REGRESSION TESTING 
20 REM OF ALL INTERPRETER FUNCTIONALITY 
30 PRINT "*Addition / Compound statements" 
40 LET I = 100 : LET J = 200 
60 PRINT ":300" 
70 PRINT I + J 
75 PRINT "*Multiplication" 
80 PRINT ":20000" 
90 PRINT I * J 
95 PRINT "*Order of operations A" 
100 PRINT ":20100" 
110 PRINT 100 + I * J 
115 PRINT "*Order of operations B" 
120 PRINT ":40000" 
130 PRINT ( 100 + I ) * J 
135 PRINT "* conditional branching IF THEN" 
136 PRINT ":200" 
140 IF I > J THEN 150 ELSE 180 
160 PRINT I 
170 GOTO 180 
180 PRINT J 
190 PRINT "* Unconditional branching GOTO" 
195 PRINT ":line220" 
200 GOTO 220 
210 PRINT "Should not print this line" 
220 PRINT "line220" 
225 REM Subroutine tests 
230 PRINT "* Gosub" 
240 GOSUB 1630 
250 PRINT "subroutine" 
260 PRINT "* Nested gosub" 
265 PRINT ":FIRST/SECOND" 
270 GOSUB 1660 
275 REM LOOP TESTS 
280 PRINT "* FOR loop, simple" 
290 PRINT ":12345" 
300 FOR I = 1 TO 5 
310 PRINT I ; 
320 NEXT I 
325 PRINT 
330 PRINT "* FOR loop, with negative step" 
335 PRINT ":108642" 
340 FOR I = 10 TO 1 STEP - 2 
350 PRINT I ; 
360 NEXT I 
365 PRINT 
370 PRINT "* Nested loops" 
375 PRINT ":111213212223" 
380 FOR I = 1 TO 2 
390 FOR J = 1 TO 3 
400 PRINT I ; J ; 
410 NEXT J 
420 NEXT I 
425 PRINT 
429 REM ARRAY TESTS 
430 PRINT "* Array dim/set/get behavior test" 
440 DIM A ( 3 , 3 ) 
450 FOR I = 0 TO 2 
460 FOR J = 0 TO 2 
470 LET A ( I , J ) = 5 
480 NEXT J 
490 NEXT I 
500 PRINT ":555" 
510 PRINT A ( 0 , 0 ) ; A ( 1 , 1 ) ; A ( 2 , 2 ) 
520 PRINT "* FILE IO Test" 
530 OPEN "REGRESSION.TXT" FOR OUTPUT AS # 1 
540 PRINT # 1 , "0123456789Hello World!" 
545 PRINT # 1 , "This is second line for testing" 
550 CLOSE # 1 
560 OPEN "REGRESSION.TXT" FOR INPUT AS # 2 
570 PRINT ":Hello World!" 
580 FSEEK # 2 , 10 
590 INPUT # 2 , A$ 
600 PRINT A$ 
800 PRINT "* DATA Test A" 
815 DATA "DATA Statement tests..." 
820 READ A$ 
825 PRINT ":DATA Statement tests..." 
830 PRINT A$ 
835 PRINT "* DATA Test B" 
840 DATA 1 , 2 , 3 
850 DATA 4 , 5 , 6 
855 DATA 1.5 , 2 , "test" 
858 PRINT ":123456" 
860 FOR I = 1 TO 3 
870 READ J , K 
880 PRINT J ; K ; 
890 NEXT I 
895 PRINT 
897 PRINT "* DATA Test C" 
900 RESTORE 840 
910 READ I , J , K 
920 PRINT ":123" 
930 PRINT I ; J ; K 
940 PRINT "* DATA Test D" 
970 RESTORE 855 
980 READ A1 , B , C$ 
985 PRINT ":Float: 1.5 Int: 2 String: test" 
990 PRINT "Float: " ; A1 ; " Int: " ; B ; " String: " ; C$ 
995 PRINT "* DATA Test E" 
1000 RESTORE 850 
1010 READ I , J , K , L 
1020 PRINT ":4561.5" 
1030 PRINT I ; J ; K ; L 
1610 REM *** Finished *** 
1620 STOP 
1630 REM A SUBROUTINE TEST 
1640 PRINT ":subroutine" 
1650 RETURN 
1660 REM AN OUTER SUBROUTINE 
1670 GOSUB 1700 
1680 PRINT "SECOND" 
1690 RETURN 
1700 REM A NESTED SUBROUTINE 
1710 PRINT "FIRST/" ; 
1720 RETURN 
