import { Container } from './styles';
import { Content } from './components/Content';
import { Header } from './components/header';
import { Spin } from 'antd';
import { useLoading, useShowUpload } from './store';
import { useMemo } from 'react';

function App() {
  const { loading } = useLoading()
  const { isShow } = useShowUpload()

  const currentComponent = useMemo(() => {
    return isShow ? <h1>Result</h1> : <Content />
  }, [isShow])
  
  return (
    <Container>
      <Spin spinning={loading}>
        <Header />
        {currentComponent}
      </Spin>
    </Container>
  )
}

export default App
