if exists("g:loaded_hello")
  finish
endif
let g:loaded_hello = 1

let s:save_cpo = &cpo
set cpo&vim

command! -nargs=? Nippo call nippo#open_nippo(<f-args>)

let &cpo = s:save_cpo
unlet s:save_cpo
