# xhtml_generator_for_epub_maker
一个用于自动完成epub制作过程中创建多个xhtml文件并添加标签的步骤并生成toc.ncx中内容的工具
操作简单便捷——
只需要修改cfg.txt中的target即可改变用于标定拆分章节位置的字符，修改inputfile可变更输入的文本文件路径与名称。
双击打开exe即可完成生成
由于sigil不允许替换ncx文件,生成结果放在了txt里,请自行复制粘贴
注意：toc.txt里的content标签的src属性没填,麻烦自己填一下。
友情提示：sigil可以直接根据toc.ncx生成目录文件toc.xhtml

A tool that can automatically complete the steps of creating multiple XHTML files and adding tags during the EPUB production process
Simple and convenient operation ——
You only need to modify the 'target' in the cfg .txt to change the characters which used to calibrate the position where the chapter will be split, and modify the 'inputfile' to change the path and name of the text file you wish to input.
Double-click to open EXE to complete the XHTML generation
Since sigil does not allow replacing .NCX file, the generated results are placed in a txt file, please copy and paste by yourself.

Attention:The src attribute of the content tag in the toc.txt file is not filled in, so please fill it in by yourself.
A reminder: sigil can directly generate directory file toc.xhtml based on toc.ncx
