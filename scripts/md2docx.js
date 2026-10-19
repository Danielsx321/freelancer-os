const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,Table,TableRow,TableCell,WidthType,ShadingType,LevelFormat,BorderStyle,ImageRun,AlignmentType}=require('docx');
const path=require('path');
// Image size from the file header (PNG or JPEG), so images keep their shape.
const imgSize=b=>{if(b[0]===0x89)return[b.readUInt32BE(16),b.readUInt32BE(20)];let o=2;while(o<b.length){const m=b[o+1],len=b.readUInt16BE(o+2);if(m>=0xC0&&m<=0xC3)return[b.readUInt16BE(o+7),b.readUInt16BE(o+5)];o+=2+len}return[800,600]};
const [,,inp,out]=process.argv;
const lines=fs.readFileSync(inp,'utf8').split('\n');
const runs=(t,bold)=>t.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(s=>s.startsWith('**')?new TextRun({text:s.slice(2,-2),bold:true}):new TextRun({text:s,bold}));
const W=9360, body=[]; let i=0, nlist=0, inList=false;
const border={style:BorderStyle.SINGLE,size:4,color:"BFBFBF"}; const borders={top:border,bottom:border,left:border,right:border};
while(i<lines.length){const l=lines[i]; if(!/^\d+\. /.test(l)&&l.trim()!=='')inList=false;
 if(l.startsWith('# ')){body.push(new Paragraph({heading:HeadingLevel.HEADING_1,children:runs(l.slice(2))}));i++;continue}
 if(l.startsWith('## ')){body.push(new Paragraph({heading:HeadingLevel.HEADING_2,children:runs(l.slice(3))}));i++;continue}
 const im=l.match(/^!\[([^\]]*)\]\(([^)]+)\)$/); if(im){const f=path.resolve(path.dirname(inp),im[2]);const d=fs.readFileSync(f);const [w,h]=imgSize(d);let sw=Math.min(600,w),sh=Math.round(h*sw/w);if(sh>380){sw=Math.round(sw*380/sh);sh=380}body.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:120,after:60},children:[new ImageRun({type:/\.png$/i.test(f)?'png':'jpg',data:d,transformation:{width:sw,height:sh}})]}));if(im[1])body.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:200},children:[new TextRun({text:im[1],italics:true,size:18,color:'666666'})]}));i++;continue}
 if(/^\d+\. /.test(l)){if(!inList){nlist++;inList=true}body.push(new Paragraph({numbering:{reference:'n',level:0,instance:nlist},children:runs(l.replace(/^\d+\. /,''))}));i++;continue}
 if(l.startsWith('### ')){body.push(new Paragraph({spacing:{before:200,after:80},children:runs(l.slice(4),true)}));i++;continue}
 if(l.startsWith('- ')){body.push(new Paragraph({numbering:{reference:'b',level:0},children:runs(l.slice(2))}));i++;continue}
 if(l.startsWith('|')){const rows=[];while(i<lines.length&&lines[i].startsWith('|')){if(!/^\|[-| ]+\|$/.test(lines[i]))rows.push(lines[i].slice(1,-1).split('|').map(c=>c.trim()));i++}
  const n=rows[0].length; const cw=n===3?[3120,3120,3120]:Array(n).fill(Math.floor(W/n)); cw[n-1]+=W-cw.reduce((a,b)=>a+b,0);
  body.push(new Table({width:{size:W,type:WidthType.DXA},columnWidths:cw,rows:rows.map((r,ri)=>new TableRow({tableHeader:ri===0,children:r.map((c,ci)=>new TableCell({borders,width:{size:cw[ci],type:WidthType.DXA},margins:{top:60,bottom:60,left:100,right:100},shading:ri===0?{type:ShadingType.CLEAR,fill:"E8EEF4",color:"auto"}:undefined,children:[new Paragraph({children:runs(c,ri===0)})]}))}))}));
  body.push(new Paragraph({}));continue}
 if(l.trim()===''){i++;continue}
 body.push(new Paragraph({spacing:{after:120},children:runs(l)}));i++}
const doc=new Document({styles:{default:{document:{run:{font:"Calibri",size:22}}},paragraphStyles:[{id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:32,bold:true,color:"1F3A5F"},paragraph:{spacing:{after:200},outlineLevel:0}},{id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:26,bold:true,color:"1F3A5F"},paragraph:{spacing:{before:280,after:120},outlineLevel:1}}]},
 numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:'left',style:{paragraph:{indent:{left:540,hanging:270}}}}]},{reference:'n',levels:[{level:0,format:LevelFormat.DECIMAL,text:'%1.',alignment:'left',style:{paragraph:{indent:{left:540,hanging:270}}}}]}]},
 sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1440,bottom:1440,left:1440,right:1440}}},children:body}]});
Packer.toBuffer(doc).then(b=>fs.writeFileSync(out,b));
