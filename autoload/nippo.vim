" :help use-cpo-save
let s:save_cpo = &cpo
set cpo&vim

execute "py3f " . g:nippo#runtime_path . "/src/entry_point.py"

function! nippo#main(...)
  if a:0 == 0
    py3 nippo_main()
  else 
    py3 nippo_main(vim.eval("a:1"))
  end
endfunction

function! nippo#tasks()
  py3 nippo_tasks()
endfunction

function! nippo#add_task()
  py3 nippo_add_task()
endfunction

function! nippo#update_tasks()
  py3 nippo_update_tasks()
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
