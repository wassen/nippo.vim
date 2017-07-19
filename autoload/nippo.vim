let s:save_cpo = &cpo
set cpo&vim

pyfile <sfile>:h:h/src/hello.py
python import vim

function! nippo#today(...)
  if a:0 == 0
    python nippo_today()
  else 
    python nippo_today(vim.eval('a:1'))
  end
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
