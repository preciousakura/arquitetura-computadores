goto main
wb 0

n ww 6
c ww 0     
start ww 2 
num ww 2
i ww 2
d ww 0

      main xmem x, n               # x = n
           ymem y, c               # y = c      
           jzxgthany x, final      # if x>y == 0 goto final
           hgetone                 # h = 1
           xmem x, start           # x = start
           movx x, i               # i = x
      loop xmem x, num             # x = num
           ymem y, i               # y = i
           jzxgthany x, ifisprime  # if x>y == 0 goto ifisprime
           xmodmem x, i            # x = x%i
           jzx x, isnotprime       # if  == 0 goto isnotprime
           xmem x, i               # x = i
           xincone                 # x = x + 1
           movx x, i               # i = x
           goto loop               # goto loop
isnotprime hgetzero                # y = 0
 ifisprime jzh y, incNum           # if y == 0, goto incNum
           xmem x, num             # x = num   
           movx x, d               # d = x
           xmem x, c               # x = c
           xincone                 # x = x + 1 
           movx x, c               # c = x
    incNum xmem x, num             # x = num
           xincone                 # x = x + 1
           movx x, num             # num = x
           goto main               # goto main
     final xmem x, d               # x = d
           movx x, n               # n = x 
           halt                    # halt


