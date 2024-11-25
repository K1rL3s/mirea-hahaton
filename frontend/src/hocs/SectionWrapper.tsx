import { FC, memo } from "react";

const SectionWrapper = (Component: FC, idName: string): FC => {
  const HOC: FC = memo(() => {
    return (
      <>
        <span className="hash-span" id={idName}>
          &nbsp;
        </span>
        <Component />
      </>
    );
  });

  return HOC;
};

export default SectionWrapper;
