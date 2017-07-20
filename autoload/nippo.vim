let s:save_cpo = &cpo
set cpo&vim

py3f <sfile>:h:h/src/hello.py
py3 import vim

function! nippo#today(...)
  if a:0 == 0
    py3  nippo_today()
  else 
    py3 nippo_today(vim.eval('a:1'))
  end
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
