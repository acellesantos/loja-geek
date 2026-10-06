let fotoAtualIndex = 0;
let listaFotosAtuais = [];
let escalaZoom = 1;

document.addEventListener("DOMContentLoaded", () => {
    // 1. Lógica de Zoom com o Scroll do Mouse no Modal
    const container = document.getElementById('modalImagemContainer');
    const img = document.getElementById('modalImagemPrincipal');

    if (container && img) {
        container.addEventListener('wheel', (e) => {
            e.preventDefault(); // Evita rolar a página por trás do modal
            
            if (e.deltaY < 0) {
                escalaZoom = Math.min(escalaZoom + 0.2, 3); // Zoom In (máx 3x)
            } else {
                escalaZoom = Math.max(escalaZoom - 0.2, 1); // Zoom Out (mín 1x)
            }
            
            img.style.transform = `scale(${escalaZoom})`;
            container.style.cursor = escalaZoom > 1 ? 'zoom-out' : 'zoom-in';
        });
    }

    // 2. Lógica de Busca em Tempo Real no Catálogo
    const searchInput = document.querySelector('.search-field input');
    const cards = document.querySelectorAll('.grid .card');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const termo = e.target.value.toLowerCase().trim();
            
            cards.forEach(card => {
                const textoCard = card.innerText.toLowerCase();
                if (textoCard.includes(termo)) {
                    card.style.display = "";
                } else {
                    card.style.display = "none";
                }
            });
        });
    }
});

function resetarZoom() {
    escalaZoom = 1;
    const img = document.getElementById('modalImagemPrincipal');
    const container = document.getElementById('modalImagemContainer');
    if (img) img.style.transform = 'scale(1)';
    if (container) container.style.cursor = 'zoom-in';
}

// 1. Adicione 'franquia' nos parâmetros recebidos pela função:
function abrirDetalhes(nome, preco, categoria, franquia, fotos, codigo, estado, condicao) {
    const modal = document.getElementById('modalDetalhes');
    if (!modal) return;

    document.getElementById('modalNome').innerText = nome;
    
    const precoFormatado = preco.startsWith('R$') ? preco : 'R$ ' + preco;
    document.getElementById('modalPreco').innerText = precoFormatado;
    
    // 2. Mude de 'produto.franquia' para apenas 'franquia':
    document.getElementById('modalBadgeFranquia').innerText = franquia || '';
    
    document.getElementById('modalBadgeCat').innerText = categoria;
    document.getElementById('modalCodigo').innerText = codigo ? 'Código ' + codigo : '';
    document.getElementById('modalEstado').innerText = estado || 'Novo';
    document.getElementById('modalCondicao').innerText = condicao || 'Caixa em bom estado de conservação.';
    
    listaFotosAtuais = (fotos && fotos.length > 0) ? fotos : ['default.jpg'];
    fotoAtualIndex = 0;
    
    resetarZoom();
    atualizarExibicaoFoto();
    
    // Configuração do botão do WhatsApp
    const btnWhats = document.getElementById('btnTenhoInteresse');
    if (btnWhats) {
        btnWhats.onclick = function() {
            const telefone = "5521999999999"; // Substitua pelo seu número real
            const mensagem = `Olá! Tenho interesse no produto ${nome} por ${precoFormatado}. Ele ainda está disponível?`;
            const url = `https://wa.me/${telefone}?text=${encodeURIComponent(mensagem)}`;
            window.open(url, '_blank');
        };
    }
    
    modal.showModal();
}

function atualizarExibicaoFoto() {
    resetarZoom();
    const imgPrincipal = document.getElementById('modalImagemPrincipal');
    const containerMiniaturas = document.getElementById('modalMiniaturas');
    if (!containerMiniaturas || !imgPrincipal) return;

    containerMiniaturas.innerHTML = '';
    
    const caminhoBase = window.caminhoImagens || 'img/';
    
    if (listaFotosAtuais.length > 0) {
        imgPrincipal.src = caminhoBase + listaFotosAtuais[fotoAtualIndex];
        
        const btnAnt = document.getElementById('btnAnterior');
        const btnProx = document.getElementById('btnProximo');
        
        if (btnAnt && btnProx) {
            if (listaFotosAtuais.length <= 1) {
                btnAnt.style.display = 'none';
                btnProx.style.display = 'none';
            } else {
                btnAnt.style.display = 'flex';
                btnProx.style.display = 'flex';
            }
        }

        listaFotosAtuais.forEach((foto, index) => {
            const btnThumb = document.createElement('button');
            const selecionada = index === fotoAtualIndex;
            btnThumb.style.cssText = "cursor: pointer; background: #fff; border: 2px solid " + (selecionada ? "#b17d12" : "transparent") + "; border-radius: 8px; width: 54px; height: 54px; padding: 2px; overflow: hidden; flex-shrink: 0;";
            
            const thumbImg = document.createElement('img');
            thumbImg.src = caminhoBase + foto;
            thumbImg.style.cssText = "object-fit: contain; width: 100%; height: 100%;";
            
            btnThumb.appendChild(thumbImg);
            btnThumb.onclick = () => {
                fotoAtualIndex = index;
                atualizarExibicaoFoto();
            };
            containerMiniaturas.appendChild(btnThumb);
        });
    }
}

function mudarFoto(direcao) {
    if (listaFotosAtuais.length === 0) return;
    fotoAtualIndex += direcao;
    if (fotoAtualIndex < 0) {
        fotoAtualIndex = listaFotosAtuais.length - 1;
    } else if (fotoAtualIndex >= listaFotosAtuais.length) {
        fotoAtualIndex = 0;
    }
    atualizarExibicaoFoto();
}

function fecharDetalhes() {
    resetarZoom();
    const modal = document.getElementById('modalDetalhes');
    if (modal) modal.close();
}

