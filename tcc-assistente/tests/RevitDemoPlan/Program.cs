using System.Text.Json;
using TccAssistente.RevitDemo;
int checks=0;
void Check(bool ok,string name){if(!ok)throw new Exception(name);checks++;}
void Reject(Action run,string name){try{run();}catch{checks++;return;}throw new Exception("Aceitou plano inválido: "+name);}
var p=DemoPlan.Example();p.RequireReady();Check(p.Preview().Contains("9 elementos"),"contagem da prévia");
var json=JsonSerializer.Serialize(p,DemoPlan.JsonOptions);Check(DemoPlan.Parse(json)==p,"contrato camelCase ida e volta");
Reject(()=>(p with{SpanXM=null}).RequireReady(),"dimensão ausente");Reject(()=>(p with{SpanXM=100}).RequireReady(),"vão fora do limite");Reject(()=>(p with{BeamBM=.1}).RequireReady(),"largura fora do limite");Reject(()=>(p with{Units="cm"}).RequireReady(),"unidades");Reject(()=>(p with{Scene="two_storeys"}).RequireReady(),"pavimentos");Reject(()=>(p with{Status="unsupported"}).RequireReady(),"recusa");Reject(()=>DemoPlan.Parse(json[..^1]+",\"code\":\"execute\"}"),"campo extra");
var pending=p with{Status="needs_clarification",SpanXM=null};pending.Validate();Check(pending.Preview()==pending.Message,"pendência sem execução");
Console.WriteLine($"{checks} verificações C# passaram. Sem execução da API do Revit ou chamada à IA.");
