let s:save_cpo = &cpo
set cpo&vim

execute "py3f " . g:nippo#runtime_path . "/src/nippo.py"
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
