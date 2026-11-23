import { CalculateMetadataFunction } from "remotion";

// Padrão de exportação das composições de overlay: ProRes 4444 com alfa.
export const calcularAlfa: CalculateMetadataFunction<{
  fundo: string | null;
}> = () => {
  return {
    defaultCodec: "prores",
    defaultVideoImageFormat: "png",
    defaultPixelFormat: "yuva444p10le",
    defaultProResProfile: "4444",
  };
};
