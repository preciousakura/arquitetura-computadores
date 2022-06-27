goto main
wb 0

menor ww 0
x1 ww 120
x2 ww 200
x3 ww 101

  main xmem x, x1
       ymem y, x2
       jzxgthany x, casox1  
       xmem x, x3  
       jzxgthany x, finalx 
       goto finaly
casox1 ymem y, x3           
       jzxgthany x, finalx
       goto finaly
finalx movx x, menor
       halt
finaly movy y, menor
       halt