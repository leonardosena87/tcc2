import AdmZip from 'adm-zip';
const xml=value=>String(value).replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g,'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
export function validateTable(table){
  if(!table||!Array.isArray(table.columns)||table.columns.length<1||table.columns.length>20||!Array.isArray(table.rows)||table.rows.length>200||table.columns.some(v=>typeof v!=='string'||v.length>1000)||table.rows.some(r=>!Array.isArray(r)||r.length!==table.columns.length||r.some(v=>typeof v!=='string'||v.length>10000)))throw new Error('Tabela inválida ou acima do limite de 200 linhas e 20 colunas.');
  return table;
}
export function createDownload({format,text,table}){
  const zip=new AdmZip();const add=(name,value)=>zip.addFile(name,Buffer.from(value));
  const rels='http://schemas.openxmlformats.org/package/2006/relationships';
  const rel='http://schemas.openxmlformats.org/officeDocument/2006/relationships';
  if(format==='docx'){
    if(typeof text!=='string'||!text.trim()||text.length>150000)throw new Error('Texto vazio ou muito longo para exportar.');
    add('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>');
    add('_rels/.rels',`<Relationships xmlns="${rels}"><Relationship Id="rId1" Type="${rel}/officeDocument" Target="word/document.xml"/></Relationships>`);
    add('word/document.xml',`<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>${text.split(/\r?\n/).map(line=>`<w:p><w:pPr><w:spacing w:after="120"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">${xml(line)}</w:t></w:r></w:p>`).join('')}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1417" w:right="1417" w:bottom="1417" w:left="1417"/></w:sectPr></w:body></w:document>`);
    return {name:'resposta-tcc.docx',mime:'application/vnd.openxmlformats-officedocument.wordprocessingml.document',base64:zip.toBuffer().toString('base64')};
  }
  if(format!=='xlsx')throw new Error('Formato de exportação inválido.');
  validateTable(table);
  add('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>');
  add('_rels/.rels',`<Relationships xmlns="${rels}"><Relationship Id="rId1" Type="${rel}/officeDocument" Target="xl/workbook.xml"/></Relationships>`);
  add('xl/workbook.xml',`<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="${rel}"><sheets><sheet name="Resultado" sheetId="1" r:id="rId1"/></sheets></workbook>`);
  add('xl/_rels/workbook.xml.rels',`<Relationships xmlns="${rels}"><Relationship Id="rId1" Type="${rel}/worksheet" Target="worksheets/sheet1.xml"/></Relationships>`);
  add('xl/worksheets/sheet1.xml',`<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" state="frozen"/></sheetView></sheetViews><cols><col min="1" max="${table.columns.length}" width="28" customWidth="1"/></cols><sheetData>${[table.columns,...table.rows].map((row,i)=>`<row r="${i+1}">${row.map((cell,j)=>`<c r="${String.fromCharCode(65+j)}${i+1}" t="inlineStr"><is><t xml:space="preserve">${xml(cell)}</t></is></c>`).join('')}</row>`).join('')}</sheetData></worksheet>`);
  return {name:'tabela-tcc.xlsx',mime:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',base64:zip.toBuffer().toString('base64')};
}
