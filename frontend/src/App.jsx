import { Routes, Route } from "react-router-dom";

import NavBar from "./components/NavBar";
import MensagemFlash from "./components/MensagemFlash";
import RotaProtegida from "./components/RotaProtegida";
import EmConstrucao from "./components/EmConstrucao";

import HomePagina from "./pages/geral/HomePagina";
import PainelAdminPagina from "./pages/geral/PainelAdminPagina";
import PaginaErro from "./pages/geral/PaginaErro";
import PontoPagina from "./pages/pontos/PontoPagina";
import FavoritoPagina from "./pages/pontos/FavoritoPagina";
import PontoAdminPagina from "./pages/pontos/PontoAdminPagina";
import SugestaoAdminPagina from "./pages/pontos/SugestaoAdminPagina";
import CategoriaPagina from "./pages/categorias/CategoriaPagina";
import EcossistemaPagina from "./pages/ecossistemas/EcossistemaPagina";
import TipoCulturalPagina from "./pages/tiposCulturais/TipoCulturalPagina";
import DestaquePagina from "./pages/destaques/DestaquePagina";
import PromocaoPagina from "./pages/promocoes/PromocaoPagina";
import UsuarioPagina from "./pages/usuarios/UsuarioPagina";
import LoginPagina from "./pages/usuarios/LoginPagina";
import CadastroPagina from "./pages/usuarios/CadastroPagina";
import RecuperarSenhaPagina from "./pages/usuarios/RecuperarSenhaPagina";
import RedefinirSenhaPagina from "./pages/usuarios/RedefinirSenhaPagina";
import SobrePagina from "./pages/geral/SobrePagina";

function App() {

  return (
    <>
      <NavBar />
      <MensagemFlash />
      <div className="container mt-5 pt-5">
        <Routes>

          {/* Públicas (qualquer pessoa) */}
          <Route path="/" element={<HomePagina />} />
          <Route path="/pontos" element={<PontoPagina />} />
          <Route path="/pontos/:id" element={<EmConstrucao titulo="Detalhes do Ponto" />} />
          <Route path="/pontos/:id/avaliacoes" element={<EmConstrucao titulo="Avaliações do Ponto" />} />
          <Route path="/pontos/:id/avaliacao/editar" element={<EmConstrucao titulo="Editar Avaliação" />} />
          <Route path="/sobre" element={<SobrePagina />} />
          <Route path="/erro" element={<PaginaErro />} />

          {/* Somente visitante (quem já está logado volta para a Home) */}
          <Route element={<RotaProtegida permissoes={["visitante"]} />}>
            <Route path="/login" element={<LoginPagina />} />
            <Route path="/cadastro" element={<CadastroPagina />} />
            <Route path="/recuperar-senha" element={<RecuperarSenhaPagina />} />
            <Route path="/redefinir-senha/:token" element={<RedefinirSenhaPagina />} />
          </Route>

          {/* Qualquer usuário logado */}
          <Route element={<RotaProtegida permissoes={["logado"]} />}>
            <Route path="/favoritos" element={<FavoritoPagina />} />
            <Route path="/editar-perfil" element={<EmConstrucao titulo="Editar Perfil" />} />
          </Route>

          {/* Somente usuário comum (user) */}
          <Route element={<RotaProtegida permissoes={["user"]} />}>
            <Route path="/sugerir-ponto" element={<EmConstrucao titulo="Sugerir Ponto" />} />
            <Route path="/sugestoes/:id/editar" element={<EmConstrucao titulo="Editar Sugestão" />} />
          </Route>

          {/* Somente admin e superadmin */}
          <Route element={<RotaProtegida permissoes={["admin", "superadmin"]} />}>
            <Route path="/admin/painel-admin" element={<PainelAdminPagina />} />

            <Route path="/admin/pontos" element={<PontoAdminPagina />} />
            <Route path="/admin/pontos/cadastrar" element={<EmConstrucao titulo="Cadastrar Ponto" />} />
            <Route path="/admin/pontos/:id/atualizar" element={<EmConstrucao titulo="Editar Ponto" />} />
            <Route path="/admin/sugestoes" element={<SugestaoAdminPagina />} />

            <Route path="/admin/categorias" element={<CategoriaPagina />} />
            <Route path="/admin/categorias/cadastrar" element={<EmConstrucao titulo="Cadastrar Categoria" />} />
            <Route path="/admin/categorias/:id/atualizar" element={<EmConstrucao titulo="Editar Categoria" />} />

            <Route path="/admin/ecossistemas" element={<EcossistemaPagina />} />
            <Route path="/admin/ecossistemas/cadastrar" element={<EmConstrucao titulo="Cadastrar Ecossistema" />} />
            <Route path="/admin/ecossistemas/:id/atualizar" element={<EmConstrucao titulo="Editar Ecossistema" />} />

            <Route path="/admin/tipos-culturais" element={<TipoCulturalPagina />} />
            <Route path="/admin/tipos-culturais/cadastrar" element={<EmConstrucao titulo="Cadastrar Tipo Cultural" />} />
            <Route path="/admin/tipos-culturais/:id/atualizar" element={<EmConstrucao titulo="Editar Tipo Cultural" />} />

            <Route path="/admin/destaques" element={<DestaquePagina />} />
            <Route path="/admin/destaques/cadastrar" element={<EmConstrucao titulo="Cadastrar Destaque" />} />
            <Route path="/admin/destaques/:id/atualizar" element={<EmConstrucao titulo="Editar Destaque" />} />

            <Route path="/admin/promocoes" element={<PromocaoPagina />} />
            <Route path="/admin/promocoes/cadastrar" element={<EmConstrucao titulo="Cadastrar Promoção" />} />
            <Route path="/admin/promocoes/:id/atualizar" element={<EmConstrucao titulo="Editar Promoção" />} />

            <Route path="/admin/usuarios" element={<UsuarioPagina />} />
          </Route>

          <Route path="*" element={<PaginaErro mensagem="Essa página não existe." />} />
        </Routes>
      </div>
    </>
  );
}

export default App;