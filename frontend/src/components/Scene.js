import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useLoader } from '@react-three/fiber';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const Model = ({ url, position, rotation, scale }) => {
  const gltf = useLoader(GLTFLoader, url);
  return <primitive object={gltf.scene} position={position} rotation={rotation} scale={scale} />;
};

const Scene = ({ modelData, isVisible }) => {
  if (!isVisible) return null;

  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <Model
        url={modelData.url}
        position={modelData.position}
        rotation={modelData.rotation}
        scale={modelData.scale}
      />
      <OrbitControls enableZoom={false} enablePan={false} />
    </Canvas>
  );
};

export default Scene;