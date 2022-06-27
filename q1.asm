goto main
wb 0

result ww 0
a ww 2000
b ww 4
c ww 100
d ww 400

    main xmem x, a 
         jzxmodtwo x, continue
         goto fail
continue xmodmem x, d
         jzx x, sucess  
         xmem x, a
         xmodmem x, c
         jzx x, final
         xmem x, a
         xdivtwo 
         jzxmodtwo x, sucess   
         goto fail      
  sucess xgetone
         goto final
    fail xgetzero
   final movx x, result
         halt





