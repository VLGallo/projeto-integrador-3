import { StyleSheet, Dimensions } from 'react-native';

export const getMotoboyStyles = (isDarkMode) => {
  const { width, height } = Dimensions.get('window');
  const isMobile = width < 600;

  return StyleSheet.create({
    container: {
      flex: 1,
      paddingHorizontal: isMobile ? 10 : 30,
    },
    headerContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginVertical: isMobile ? 8 : 10,
    },
    titulo: {
      fontSize: isMobile ? 24 : 32,
      fontWeight: 'bold',
      color: isDarkMode ? '#FFF' : '#C62828',
    },
    conteudo: {
      flex: 1,
      flexDirection: 'row',
      gap: isMobile ? 6 : 10,
    },
    areaScroll: {
      flex: 1,
      paddingRight: 5,
      height: height - 130,
      backgroundColor: isDarkMode ? '#111' : '#fff',
      scrollbarColor: isDarkMode ? '#fff #222' : '#000 #fff',
      scrollbarWidth: 'thin',
    },
    areaResumo: {
      flex: 1,
      justifyContent: 'flex-end',
      alignItems: 'center',
      paddingBottom: isMobile ? 1 : 20,
    },
    scrollContainer: {
      flexGrow: 1,
      paddingBottom: isMobile ? 16 : 20,
      backgroundColor: isDarkMode ? '#222' : '#fff',
    },
    cardPedido: {
      backgroundColor: isDarkMode ? '#333' : '#fff',
      padding: isMobile ? 10 : 15,
      marginBottom: isMobile ? 8 : 10,
      borderRadius: 10,
      elevation: 3,
      flexDirection: 'row',
      justifyContent: 'space-between',
      borderWidth: isDarkMode ? 0 : 1,
      borderColor: isDarkMode ? 'transparent' : '#000',
    },
    cardEntregue: {
      opacity: 0.6,
    },
    pedidoInfo: {
      flex: 2,
    },
    pedidoTitulo: {
      fontSize: isMobile ? 16 : 20,
      fontWeight: 'bold',
      color: isDarkMode ? '#90ee90' : '#81C784',
    },
    descricao: {
      fontSize: isMobile ? 12 : 14,
      color: isDarkMode ? '#fff' : '#333',
      marginTop: 4,
    },
    botoesContainer: {
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 1, // <-- evita ultrapassar
      maxWidth: isMobile ? 60 : 80, // <-- restringe a largura total
    },
    botaoVerde: {
      backgroundColor: '#4CAF50',
      width: isMobile ? 30 : 40,
      height: isMobile ? 30 : 40,
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
    },
    botaoCinza: {
      backgroundColor: '#BDBDBD',
      width: isMobile ? 30 : 40,
      height: isMobile ? 30 : 40,
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
    },
    textoBotao: {
      fontSize: isMobile ? 12 : 16,
      color: '#fff',
    },
    resumoTexto: {
      fontSize: isMobile ? 12 : 16,
      fontWeight: 'bold',
      color: isDarkMode ? '#FFF' : '#000',
      marginTop: 10,
    },
    resumoValor: {
      fontSize: isMobile ? 16 : 18,
      fontWeight: 'bold',
      color: isDarkMode ? '#FFF' : '#C62828',
    },
    pizzaIcon: {
      width: isMobile ? 40 : 100,
      height: isMobile ? 40 : 100,
      marginTop: 10,
      resizeMode: 'contain',
    },
    faviconIcon: {
      width: isMobile ? 150 : 350,
      height: isMobile ? 150 : 350,
      marginTop: isMobile ? -20 : -40,
      alignSelf: 'center',
      resizeMode: 'contain',
    },
    caixaBranca: {
      backgroundColor: isDarkMode ? '#000' : '#FFF',
      paddingHorizontal: isMobile ? 4 : 10,
      paddingVertical: isMobile ? 4 : 6,
      borderRadius: 10,
      marginVertical: isMobile ? 4 : 6,
      alignItems: 'center',
      elevation: 4,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.2,
      shadowRadius: 3,
    },
    colunasResumo: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      gap: isMobile ? 12 : 20,
    },
    colunaItem: {
      alignItems: 'center',
    },
    statusTexto: {
      fontWeight: 'bold',
      marginTop: 4,
      fontSize: isMobile ? 12 : 14,
    },
    statusEntregue: {
      color: '#00E676',
    },
    statusCancelado: {
      color: '#FF1744',
    },
    statusPendente: {
      color: '#FF9100',
    },
  });
};
