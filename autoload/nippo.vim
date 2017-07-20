let s:save_cpo = &cpo
set cpo&vim

py3f <sfile>:h:h/src/nippo.py
py3 import vim

function! nippo#open_nippo(...)
  if a:0 == 0
    py3  open_nippo()
  else 
    py3 open_nippo(vim.eval('a:1'))
  end
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
