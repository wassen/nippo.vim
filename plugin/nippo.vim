if exists("g:nippo#loaded")
  finish
endif
let g:nippo#loaded = 1

let g:nippo#runtime_path = expand("<sfile>:h:h")
" let g:nippo#home_directory= vim.eval("g:nippo#directory"), "nippo"

let s:save_cpo = &cpo
set cpo&vim

command! -nargs=? Nippo call nippo#main(<f-args>)
command! -nargs=0 NippoTasks call nippo#tasks(<f-args>)
command! -nargs=0 TaskAdd call nippo#add_task(<f-args>)

let &cpo = s:save_cpo
unlet s:save_cpo

autocmd BufWritePre */nippo/*/*.md call nippo#add_task()
" nippoで固定する、Python側で判断する
" */nippo/*/*.md
