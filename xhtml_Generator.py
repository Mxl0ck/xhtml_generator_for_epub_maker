#__*__ coding: utf-8 __*__
import re 
import linecache
import docx
import os

with open('cfg.txt','r',encoding='utf-8') as file:
    l=file.readlines()
    d={}
    for i in l:
        s=i.replace('\n','')
        s0=s.split(sep=':')
        if '"' in s0[1]:
            s0[1]=s0[1].replace('"','')
        else:
            s0[1]=int(s0[1])
        d[s0[0]]=s0[1]

inputfile = d['inputfile']
target = d['target']
filename,extension = os.path.splitext(inputfile)
number = []
conttext =[]
lineCounter = 1
size = 0
s_path = ".\\output\\"  #xhtml文件的存放路径 The path where the .xhtml file are stored    
i_path = ".\\input\\"

if extension == '.docx':
    docfile=docx.Document(inputfile)
    temp_out=open(i_path+'temp.txt','w',encoding='utf-8')
    for para in docfile.paragraphs:
        temp_out.write(para.text+'\n')
    temp_out.close()
    inputfile='.\\input\\temp.txt'
elif extension == '.txt':
    inputfile=inputfile

#输入源文件Input files
head=open("head.txt","r")
toc_head=open("toc_head.txt",'r')
headtext=head.read()
toc_headtext=toc_head.read()
with open(inputfile,'r',encoding='utf-8') as fp:
    for eachLine in fp:        
        m = re.search(target, eachLine) #搜索关键字,用于拆分章节 Search for keywords which will be used to split chapters
        if m is not None:
            number.append(lineCounter) #将关键字的行号记录在number中 Record the line number of the keyword in number
        lineCounter = lineCounter + 1

#生成正文xhtml Generate the body xhtml
def gen_xhtml():
    if len(number):
        size = int(len(number))
        for i in range(0,size-1):
            start = number[i]
            end = number[i+1]
            destLines = linecache.getlines(inputfile)[start:end-1]#将行号为start到end-1的文件内容截取出来 Intercept the contents of the file with the line number 'start' to 'end-1'
            path = s_path + str(i+1) + '.xhtml'
            fp_w = open(path,'w',encoding='utf-8') #将截取出的内容保存在xhtml中 Save the extracted content in .XHTML
            fp_w.write(headtext)
            for word in destLines:
                words=word.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                fp_w.write('\n'+'<p>'+ words +'</p>')
            fp_w.write('\n'+'</body>'+'\n'+'</html>')
            fp_w.close()
            if i+2 == int(len(number)):
                path1 = s_path + str(i+2)+ '.xhtml'
                fp_end = open(path1,'w',encoding='utf-8')
                lines = linecache.getlines(inputfile)[number[i+1]+1:int(lineCounter)]
                fp_end.write(headtext)
                for word in lines:
                    words=word.strip().replace(' ', '').replace('\n', '').replace('\r', '')
                    fp_end.write('\n'+'<p>'+ words +'</p>')
                fp_end.write('\n'+'</body>'+'\n'+'</html>')
                fp_end.close()
            
    else:
        size = int(lineCounter)
        for i in range(0,size-1):
            end = int(lineCounter)
            destLines = linecache.getlines(inputfile)[0:end]
            fp_w = open('.\\output\\1.xhtml','w',encoding='utf-8')
            fp_w.write(headtext)
            for word in destLines:
                words=word.strip().replace(' ', '').replace('\n', '').replace('\r', '')
                fp_w.write('\n'+'<p>'+ words +'</p>')
            fp_w.write('\n'+'</body>'+'\n'+'</html>')
            fp_w.close()
    linecache.clearcache()

#生成toc.ncx Build toc.ncx
def gen_toc():
    if len(number):
        path = s_path + "toc" + '.txt'
        cont=open(path,'w',encoding='utf-8')
        cont.write(toc_headtext)
        i=1
        for line in number:
            word=linecache.getline(inputfile,line)#获取关键字所在行的内容 Gets the contents of the row where the keyword is located
            words=word.strip().replace(' ', '').replace('\n', '').replace('\r', '')
            cont.write('\n'+'<navPoint id="navPoint-'+str(i)+'" playOrder="'+str(i)+'">'+'\n'+'<navLabel>'+'\n'+'<text>'+ words +'</text>'+'\n'+'</navLabel>'+'\n'+'<content src="Text/.xhtml"/>'+'\n'+'</navPoint>')
            i+=1
        cont.write('\n'+'  </navMap>'+'\n'+'</ncx>')
        cont.close()
        linecache.clearcache()
        print("目录里的content标签的src属性没填,麻烦自己填一下。由于sigil不允许替换ncx文件,生成结果放在了txt里,请自行复制粘贴")
        print("The src attribute of the content tag in the toc file is not filled in, so please fill it in by yourself.Since sigil does not allow replacing .NCX file, the generated results are placed in a txt file, please copy and paste by yourself")

#删除临时文件（如果有） Delete temporary files (if it exist)
def del_temp():
    path = ".\\input"
    filelist=os.listdir(path)
    for i in filelist:
        if i == "temp.txt":
            os.remove(".\\input\\temp.txt")
        else:
            pass
        
if __name__ == "__main__":
    gen_xhtml()
    gen_toc()
    del_temp()