let s:save_cpo = &cpo
set cpo&vim

execute "py3f " . g:nippo#runtime_path . "/src/nippo.py"
py3 import vim

function! nippo#open(...)
  if a:0 == 0
    py3  Nippo().open()
  else 
    py3 Nippo(vim.eval('a:1')).open()
  end
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
