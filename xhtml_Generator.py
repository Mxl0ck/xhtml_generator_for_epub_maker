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
    
#变量赋值
inputfile = d['inputfile']
target = d['target']
filename,extension = os.path.splitext(inputfile)
number = []
lineNumber = 1
size = 0
s_path = ".\\output\\"  #xhtml文件的存放路径 The path where the .xhtml file are stored    
i_path = ".\\input\\"

if extension == '.docx':
    docfile=docx.Document(inputfile)
    temp_out=open(i_path+'temp.txt','w',encoding='utf-8')
    for para in docfile.paragraphs:
        temp_out.write(para.text+'\n')
        temp_out.close
    inputfile='.\\input\\temp.txt'
elif extension == '.txt':
    inputfile=inputfile
fp=open(inputfile,'r',encoding='utf-8')#输入源文件Input files
head=open("head.txt","r")
headtext=head.read()

for eachLine in fp:        
    m = re.search(target, eachLine) #搜索关键字,用于拆分章节 Search for keywords which Used to split chapters
    if m is not None:
        number.append(lineNumber) #将关键字的行号记录在number中 Record the line number of the keyword in number
    lineNumber = lineNumber + 1

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
            lines = linecache.getlines(inputfile)[number[i+1]+1:int(lineNumber)]
            fp_end.write(headtext)
            for word in lines:
                words=word.strip().replace(' ', '').replace('\n', '').replace('\r', '')
                fp_end.write('\n'+'<p>'+ words +'</p>')
            fp_end.write('\n'+'</body>'+'\n'+'</html>')
            fp_end.close()
        
else:
    size = int(lineNumber)
    for i in range(0,size-1):
        end = int(lineNumber)
        destLines = linecache.getlines(inputfile)[0:end]
        fp_w = open('.\\output\\1.xhtml','w',encoding='utf-8')
        fp_w.write(headtext)
        for word in destLines:
            words=word.strip().replace(' ', '').replace('\n', '').replace('\r', '')
            fp_w.write('\n'+'<p>'+ words +'</p>')
        fp_w.write('\n'+'</body>'+'\n'+'</html>')
        fp_w.close()
os.remove(i_path+'temp.txt')