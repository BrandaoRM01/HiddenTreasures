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
import PontoCadastro from "./pages/pontos/PontoCadastro";
import PontoAtualizar from "./pages/pontos/PontoAtualizar";
import SugerirPontoPagina from "./pages/pontos/SugerirPontoPagina";
import SugestaoAtualizar from "./pages/pontos/SugestaoAtualizar";
import EditarPerfilPagina from "./pages/usuarios/EditarPerfilPagina";
import SugestaoAdminPagina from "./pages/pontos/SugestaoAdminPagina";
import CategoriaPagina from "./pages/categorias/CategoriaPagina";
import CategoriaCadastro from "./pages/categorias/CategoriaCadastro";
import CategoriaAtualizar from "./pages/categorias/CategoriaAtualizar";
import EcossistemaPagina from "./pages/ecossistemas/EcossistemaPagina";
import EcossistemaCadastro from "./pages/ecossistemas/EcossistemaCadastro";
import EcossistemaAtualizar from "./pages/ecossistemas/EcossistemaAtualizar";
import TipoCulturalPagina from "./pages/tiposCulturais/TipoCulturalPagina";
import TipoCulturalCadastro from "./pages/tiposCulturais/TipoCulturalCadastro";
import TipoCulturalAtualizar from "./pages/tiposCulturais/TipoCulturalAtualizar";
import DestaquePagina from "./pages/destaques/DestaquePagina";
import DestaqueCadastro from "./pages/destaques/DestaqueCadastro";
import DestaqueAtualizar from "./pages/destaques/DestaqueAtualizar";
import PromocaoPagina from "./pages/promocoes/PromocaoPagina";
import PromocaoCadastro from "./pages/promocoes/PromocaoCadastro";
import PromocaoAtualizar from "./pages/promocoes/PromocaoAtualizar";
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
            <Route path="/editar-perfil" element={<EditarPerfilPagina />} />
          </Route>

          {/* Somente usuário comum (user) */}
          <Route element={<RotaProtegida permissoes={["user"]} />}>
            <Route path="/sugerir-ponto" element={<SugerirPontoPagina />} />
            <Route path="/sugestoes/:id/editar" element={<SugestaoAtualizar />} />
          </Route>

          {/* Somente admin e superadmin */}
          <Route element={<RotaProtegida permissoes={["admin", "superadmin"]} />}>
            <Route path="/admin/painel-admin" element={<PainelAdminPagina />} />

            <Route path="/admin/pontos" element={<PontoAdminPagina />} />
            <Route path="/admin/pontos/cadastrar" element={<PontoCadastro />} />
            <Route path="/admin/pontos/:id/atualizar" element={<PontoAtualizar />} />
            <Route path="/admin/sugestoes" element={<SugestaoAdminPagina />} />

            <Route path="/admin/categorias" element={<CategoriaPagina />} />
            <Route path="/admin/categorias/cadastrar" element={<CategoriaCadastro />} />
            <Route path="/admin/categorias/:id/atualizar" element={<CategoriaAtualizar />} />

            <Route path="/admin/ecossistemas" element={<EcossistemaPagina />} />
            <Route path="/admin/ecossistemas/cadastrar" element={<EcossistemaCadastro />} />
            <Route path="/admin/ecossistemas/:id/atualizar" element={<EcossistemaAtualizar />} />

            <Route path="/admin/tipos-culturais" element={<TipoCulturalPagina />} />
            <Route path="/admin/tipos-culturais/cadastrar" element={<TipoCulturalCadastro />} />
            <Route path="/admin/tipos-culturais/:id/atualizar" element={<TipoCulturalAtualizar />} />

            <Route path="/admin/destaques" element={<DestaquePagina />} />
            <Route path="/admin/destaques/cadastrar" element={<DestaqueCadastro />} />
            <Route path="/admin/destaques/:id/atualizar" element={<DestaqueAtualizar />} />

            <Route path="/admin/promocoes" element={<PromocaoPagina />} />
            <Route path="/admin/promocoes/cadastrar" element={<PromocaoCadastro />} />
            <Route path="/admin/promocoes/:id/atualizar" element={<PromocaoAtualizar />} />

            <Route path="/admin/usuarios" element={<UsuarioPagina />} />
          </Route>

          <Route path="*" element={<PaginaErro mensagem="Essa página não existe." />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
