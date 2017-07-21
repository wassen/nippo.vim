if exists("g:nippo#loaded")
  finish
endif
let g:nippo#loaded = 1

let g:nippo#runtime_path = expand("<sfile>:h:h")

let s:save_cpo = &cpo
set cpo&vim

command! -nargs=? Nippo call nippo#open_nippo(<f-args>)

let &cpo = s:save_cpo
unlet s:save_cpo
