import { Composition, Folder, staticFile } from "remotion";
import {
  CaptionedVideo,
  calculateCaptionedVideoMetadata,
  captionedVideoSchema,
} from "./CaptionedVideo";
import {
  ComparacaoLadoALado,
  comparacaoSchema,
} from "./ComparacaoLadoALado";
import { MitoApego } from "./MitoApego";
import { MitoRindo } from "./MitoRindo";
import { IrEmbora } from "./TipoCinetica/IrEmbora";
import { VoceSoVolta } from "./TipoCinetica/VoceSoVolta";
import { CREME, DURACAO, FPS } from "./TipoCinetica/quadro";
import { calcularAlfa } from "./TipoCinetica/alfa";

// Each <Composition> is an entry in the sidebar!

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CaptionedVideo"
        component={CaptionedVideo}
        calculateMetadata={calculateCaptionedVideoMetadata}
        schema={captionedVideoSchema}
        width={1080}
        height={1920}
        defaultProps={{
          src: staticFile("sample-video.mp4"),
        }}
      />
      <Composition
        id="ComparacaoLadoALado"
        component={ComparacaoLadoALado}
        schema={comparacaoSchema}
        durationInFrames={360}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          rotuloEsquerda: "Lado A",
          rotuloDireita: "Lado B",
          corDestaque: "#c83c1e",
        }}
      />
      <Composition
        id="MitoRindo"
        component={MitoRindo}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="MitoApego"
        component={MitoApego}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
      />
      <Folder name="Tipografia-cinetica">
        {/* Overlay com fundo transparente: exporta em ProRes 4444 com alfa. */}
        <Composition
          id="IrEmbora"
          component={IrEmbora}
          calculateMetadata={calcularAlfa}
          durationInFrames={DURACAO}
          fps={FPS}
          width={1080}
          height={1920}
          defaultProps={{ fundo: null }}
        />
        {/* A mesma batida sobre o creme, só para conferir. */}
        <Composition
          id="IrEmboraCreme"
          component={IrEmbora}
          durationInFrames={DURACAO}
          fps={FPS}
          width={1080}
          height={1920}
          defaultProps={{ fundo: CREME }}
        />
        <Composition
          id="VoceSoVolta"
          component={VoceSoVolta}
          calculateMetadata={calcularAlfa}
          durationInFrames={DURACAO}
          fps={FPS}
          width={1080}
          height={1920}
          defaultProps={{ fundo: null }}
        />
        <Composition
          id="VoceSoVoltaCreme"
          component={VoceSoVolta}
          durationInFrames={DURACAO}
          fps={FPS}
          width={1080}
          height={1920}
          defaultProps={{ fundo: CREME }}
        />
      </Folder>
    </>
  );
};
