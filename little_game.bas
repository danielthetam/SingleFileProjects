0 'My first venture into BASIC. This is written in MSX BASIC, and can be run using an MSX emulator, like MSXPen
1 'It is a very simple ASCII console game. Written with little to no knowledge of BASIC.
10 X=12 'player X position
20 Y=2 'player Y position
21 K=20 'goal X pos
22 Z=12 'goal Y pos
23 S=-1 'current sign for rng
24 J=0 'player score
25 CLS
26 LOCATE 0, 0
27 PRINT J
30 LOCATE X, Y
35 PRINT "O"
38 LOCATE K, Z
39 PRINT "X"
40 A$=INKEY$
50 IF A$="d" AND (X+1)<35 THEN GOSUB 80
51 IF A$="a" AND (X-1)>1 THEN GOSUB 100
52 IF A$="s" AND (Y+1)<22 THEN GOSUB 140
53 IF A$="w" AND (Y-1)>1 THEN GOSUB 190
55 IF X=K AND Y=Z THEN GOSUB 240
60 GOTO 30
70 END
75 REM Go right routine
80 LOCATE X, Y 
81 PRINT " "
85 X=X+1
90 RETURN
95 REM Go left routine
100 LOCATE X, Y
110 PRINT " "
120 X=X-1
130 RETURN
135 REM Go down routine
140 LOCATE X, Y
150 PRINT " "
170 Y=Y+1
180 RETURN
185 REM Go up routine
190 LOCATE X, Y
200 PRINT " "
220 Y=Y-1
230 RETURN
235 REM Below is the routine for when the player scores
240 PLAY "CEGO5CO4"
241 LOCATE 0, 0
242 J=J+1
243 PRINT J
261 LOCATE K, Z
262 PRINT " "
263 GOSUB 300 'call rng sign routine
264 O=INT(RND(-TIME) * 5) * S
265 GOSUB 300
266 P=INT(RND(-TIME) * 5) * S
270 IF (K+O)<35 AND (K+O)>1THEN K=K+O ELSE K=K-O
280 IF (Z+P)<22 AND (Z+P)>1 THEN Z=Z+P ELSE Z=Z-P
290 RETURN
295 REM Below is the rng sign generator (generates +1 or -1)
300 R=INT(RND(-TIME)*2)
310 IF R=1 THEN S=1
320 IF R=0 THEN S=-1
330 RETURN
