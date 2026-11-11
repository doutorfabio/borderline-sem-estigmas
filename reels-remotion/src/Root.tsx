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
    </>
  );
};
