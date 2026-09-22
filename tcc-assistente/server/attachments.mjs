export const FILE_LIMIT = 10 * 1024 * 1024;
export const TOTAL_LIMIT = 20 * 1024 * 1024;
export const FILE_TYPES = {
  pdf:'application/pdf', doc:'application/msword',
  docx:'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  xls:'application/vnd.ms-excel', xlsx:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
};
export function validateAttachments(files = []) {
  if(!Array.isArray(files)||files.length>5) throw new Error('Anexe no máximo 5 arquivos.');
  let total=0;
  return files.map(file=>{
    if(!file || typeof file.name!=='string' || !file.name.trim() || file.name.length>180 || /[\\/\x00-\x1f]/.test(file.name)) throw new Error('Nome de arquivo inválido.');
    const extension=file.name.split('.').at(-1).toLowerCase();
    if(!FILE_TYPES[extension]) throw new Error('Use arquivos PDF, Word (.doc/.docx) ou Excel (.xls/.xlsx).');
    if(typeof file.base64!=='string'||file.base64.length>Math.ceil(FILE_LIMIT/3)*4 || file.base64.length%4!==0 || !/^[A-Za-z0-9+/]*={0,2}$/.test(file.base64)) throw new Error('Arquivo inválido ou maior que 10 MB.');
    const bytes=Buffer.from(file.base64,'base64');total+=bytes.length;
    if(!bytes.length||bytes.length>FILE_LIMIT||total>TOTAL_LIMIT) throw new Error('Limite de 10 MB por arquivo e 20 MB por pedido.');
    const valid=extension==='pdf'?bytes.subarray(0,5).toString()==='%PDF-':
      ['docx','xlsx'].includes(extension)?bytes.subarray(0,4).equals(Buffer.from([80,75,3,4])):
      bytes.subarray(0,8).equals(Buffer.from([208,207,17,224,161,177,26,225]));
    if(!valid) throw new Error(`O conteúdo de ${file.name} não corresponde ao formato informado. Exporte novamente o arquivo.`);
    return {name:file.name,base64:file.base64,mime:FILE_TYPES[extension],size:bytes.length};
  });
}
