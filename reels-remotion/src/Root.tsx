import { Composition, staticFile } from "remotion";
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
import { IrEmbora, IrEmboraTexto } from "./IrEmbora/IrEmbora";
import { IrEmboraCapa } from "./IrEmbora/Capa";
import { Sticker } from "./IrEmbora/Sticker";

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
        id="IrEmbora"
        component={IrEmbora}
        durationInFrames={1291}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="StickerBorderline"
        component={Sticker}
        durationInFrames={1}
        fps={30}
        width={2048}
        height={1024}
        defaultProps={{ texto: "BORDERLINE", vermelho: true, id: 11 }}
      />
      <Composition
        id="StickerBipolar"
        component={Sticker}
        durationInFrames={1}
        fps={30}
        width={2048}
        height={1024}
        defaultProps={{ texto: "BIPOLAR", vermelho: false, id: 23 }}
      />
      <Composition
        id="IrEmboraCapa"
        component={IrEmboraCapa}
        durationInFrames={60}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="IrEmboraTexto"
        component={IrEmboraTexto}
        durationInFrames={1291}
        fps={30}
        width={1080}
        height={1920}
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
    </>
  );
};
