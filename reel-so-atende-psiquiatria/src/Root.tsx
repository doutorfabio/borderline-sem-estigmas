import React from "react";
import { Composition, staticFile } from "remotion";
import { loadFont } from "@remotion/fonts";
import { Reel } from "./Reel";
import timeline from "./timeline.json";

loadFont({ family: "Archivo Black", url: staticFile("fonts/ArchivoBlack.woff2"), weight: "400" });
loadFont({ family: "Poppins", url: staticFile("fonts/Poppins-400.woff2"), weight: "400" });
loadFont({ family: "Poppins", url: staticFile("fonts/Poppins-600.woff2"), weight: "600" });
loadFont({ family: "Poppins", url: staticFile("fonts/Poppins-700.woff2"), weight: "700" });

export const RemotionRoot: React.FC = () => (
  <Composition id="Reel" component={Reel} durationInFrames={timeline.total} fps={30} width={1080} height={1920} />
);
