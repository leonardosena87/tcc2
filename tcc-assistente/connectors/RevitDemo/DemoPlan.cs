using System.Globalization;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace TccAssistente.RevitDemo;

public sealed record DemoPlan(string Status,string Message,string Scene,string Units,
    double? SpanXM,double? SpanYM,double? StoreyHeightM,double? BaseZM,
    double? ColumnBM,double? ColumnHM,double? BeamBM,double? BeamHM,double? SlabHM)
{
    public const string PromptExample="Crie um pórtico didático retangular de um pavimento, com 6 x 4 m entre eixos. Base em 0,20 m e topo em 3,20 m, altura de 3 m. Use quatro pilares de 20 x 30 cm nos cantos, quatro vigas de borda de 20 x 40 cm e uma laje maciça de 14 cm. São nove elementos. Exiba em 3D. As dimensões são ilustrativas, sem dimensionamento estrutural.";
    public static readonly JsonSerializerOptions JsonOptions=new(JsonSerializerDefaults.Web){PropertyNameCaseInsensitive=false,UnmappedMemberHandling=JsonUnmappedMemberHandling.Disallow};
    public static DemoPlan Example()=>new("ready","Exemplo ensaiado. Automação local, sem chamada à IA.","rectangular_single_bay","m",6,4,3,.2,.2,.3,.2,.4,.14);
    public static DemoPlan Parse(string json){var plan=JsonSerializer.Deserialize<DemoPlan>(json,JsonOptions)??throw new InvalidDataException("Prévia vazia.");plan.Validate();return plan;}
    public void Validate()
    {
        if(Status is not ("ready" or "needs_clarification" or "unsupported")||Scene!="rectangular_single_bay"||Units!="m"||Message is null||Message.Length>3000)throw new InvalidDataException("Formato da prévia inválido.");
        var values=new(double? Value,double Min,double Max,string Name)[]{(SpanXM,1,12,"vão X"),(SpanYM,1,12,"vão Y"),(StoreyHeightM,2,5,"altura"),(BaseZM,-1,3,"cota da base"),(ColumnBM,.19,1,"largura do pilar"),(ColumnHM,.19,1,"altura da seção do pilar"),(BeamBM,.12,1,"largura da viga"),(BeamHM,.16,1.2,"altura da viga"),(SlabHM,.08,.4,"espessura da laje")};
        foreach(var (value,min,max,name) in values){if(value is null&&Status!="ready")continue;if(value is not double n||!double.IsFinite(n)||n<min||n>max)throw new InvalidDataException("Dimensão fora dos limites da demonstração: "+name);}
        if(Status=="ready"&&ColumnBM*ColumnHM<.036-1e-9)throw new InvalidDataException("Pilar fora da triagem geométrica da demonstração.");
    }
    public void RequireReady(){Validate();if(Status!="ready")throw new InvalidOperationException(Message);}
    public string Preview()
    {
        Validate();if(Status!="ready")return Message;
        var c=CultureInfo.GetCultureInfo("pt-BR");string F(double? n)=>n!.Value.ToString("0.###",c);string Cm(double? n)=>(n!.Value*100).ToString("0.##",c);
        return $"{Message}\n\nPórtico: {F(SpanXM)} × {F(SpanYM)} m entre eixos\nBase: {F(BaseZM)} m   Topo: {F(BaseZM+StoreyHeightM)} m\n4 pilares: {Cm(ColumnBM)} × {Cm(ColumnHM)} cm\n4 vigas: {Cm(BeamBM)} × {Cm(BeamHM)} cm\n1 laje: {Cm(SlabHM)} cm\n\n9 elementos em um novo arquivo de demonstração.\nDimensões ilustrativas. Sem dimensionamento estrutural.";
    }
}
