if exists("g:nippo#loaded")
  finish
endif
let g:nippo#loaded = 1

let g:nippo#runtime_path = expand("<sfile>:h:h")

" :help use-cpo-save
let s:save_cpo = &cpo
set cpo&vim

command! -nargs=? Nippo call nippo#main(<f-args>)
command! -nargs=0 NippoTasks call nippo#tasks(<f-args>)

let &cpo = s:save_cpo
unlet s:save_cpo

augroup nippo_plugin
  autocmd!
  autocmd BufWritePre */nippo/*/*.md call nippo#add_task()
  " nippoで固定する、Python側で判断する
  autocmd TextChanged *.nptsk call nippo#update_tasks()
augroup END
