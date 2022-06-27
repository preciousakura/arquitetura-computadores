goto main
wb 0

n ww 64
i ww 0
ii ww 0

 main xmem x, ii          # x = ii
      ymem y, n           # y = n
      hmem h, i           # h = i
 loop jzxgthany x, calc   # if X > Y = 0 then goto address
      hdecone
      movh h, n
      halt
 calc xplush
      addtox x, i
      hincone
      movh h, i
      goto loop
