import { IoClose } from "react-icons/io5"; // Uma opção de ícone de fechar

interface PolicyModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function PolicyModal({ isOpen, onClose }: PolicyModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-brand-dark/95 backdrop-blur-md animate-in fade-in duration-300">
      <div className="bg-brand-surface border border-brand-border w-full max-w-2xl flex flex-col max-h-[85vh] rounded-3xl shadow-2xl overflow-hidden">
        
        {/* Cabeçalho */}
        <div className="sticky top-0 bg-brand-surface p-8 pb-4 flex justify-between items-center border-b border-brand-border z-10">
          <h2 className="text-2xl font-black text-brand-primary uppercase italic">Política de Privacidade</h2>
          <button onClick={onClose} className="text-brand-muted hover:text-white p-2">
            <IoClose size={24} />
          </button>
        </div>

        {/* Conteúdo (O texto longo que você já tem) */}
        <div className="flex-1 overflow-y-auto p-8 pt-6 space-y-6 text-brand-text/90 text-sm leading-relaxed">
           <h3 className="text-brand-secondary font-bold text-lg">1. Aceitação</h3>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum fuga rerum hic molestiae esse exercitationem eaque, iusto aperiam voluptatem corrupti. Fugiat, veniam odio laudantium incidunt labore quia ipsam sed corporis.</p>
           {/* ... */}
        </div>

        {/* Rodapé */}
        <div className="p-6 bg-brand-dark/40 border-t border-brand-border flex justify-end">
          <button 
            onClick={onClose}
            className="bg-brand-primary hover:bg-brand-primary/80 text-white px-8 py-3 rounded-2xl font-bold text-sm transition-all"
          >
            ACEITAR E FECHAR
          </button>
        </div>
      </div>
    </div>
  );
}
