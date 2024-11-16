import { Box, useTexture } from "@react-three/drei";

export default function Planet() {
  const coloMap = useTexture("tierra.jpg");

  return (
    <Box args={[1, 1, 1]}>
      <meshStandardMaterial map={coloMap} />
    </Box>
  );
}
