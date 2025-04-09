import { StyleSheet, Dimensions } from 'react-native';
export const getMotoboyStyles = (isDarkMode) => styles = StyleSheet.create({
    container: {
      flex: 1,
      paddingHorizontal: 10,
    },
    headerContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginVertical: 10,
    },
    titulo: {
      fontSize: 32,
      fontWeight: 'bold',
      color: isDarkMode ? '#FFF' : '#C62828',
    },
    conteudo: {
      flex: 1,
      flexDirection: 'row',
      gap: 10,
    },
    areaScroll: {
      flex: 1,
      paddingRight: 5,
      height: Dimensions.get('window').height - 130,
      backgroundColor: isDarkMode ? '#111' : '#fff',
      scrollbarColor: isDarkMode ? '#fff #222' : '#000 #fff',
      scrollbarWidth: 'thin',
    },
    areaResumo: {
      flex: 1,
      justifyContent: 'flex-end',
      alignItems: 'center',
      paddingBottom: 20,
    },
    scrollContainer: {
      flexGrow: 1,
      paddingBottom: 20,
      backgroundColor: isDarkMode ? '#222' : '#fff',
    },
    cardPedido: {
      backgroundColor: isDarkMode ? '#333' : '#fff',
      padding: 15,
      marginBottom: 10,
      borderRadius: 10,
      elevation: 3,
      flexDirection: 'row',
      justifyContent: 'space-between',
      borderWidth: isDarkMode ? 0 : 1,
      borderColor: isDarkMode ? 'transparent' : '#000',
    },
    cardEntregue: {
      opacity: isDarkMode ? 0.6 : 0.6, // Dark / white mode
    },
    pedidoInfo: {
      flex: 2,
    },
    pedidoTitulo: {
      fontSize: 20,
      fontWeight: 'bold',
      color: isDarkMode ? '#90ee90' : '#81C784',
    },
    descricao: {
      fontSize: 14,
      color: isDarkMode ? '#fff' : '#333',
      marginTop: 4,
    },
    botoesContainer: {
      flexDirection: 'column',
      alignItems: 'center', // Centraliza no eixo horizontal
      justifyContent: 'center', // Centraliza no eixo vertical, se precisar
      gap: 8,
      marginLeft: 0, // Removido o deslocamento lateral
    },
    botaoVerde: {
      backgroundColor: '#4CAF50',
      width: 40,
      height: 40,
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
    },
    botaoCinza: {
      backgroundColor: '#BDBDBD',
      width: 40,
      height: 40,
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
    },
    textoBotao: {
      fontSize: 16,
      color: '#fff',
    },
    resumoTexto: {
      fontSize: 16,
      fontWeight: 'bold',
      color: '#000',
      marginTop: 10,
    },
    resumoValor: {
      fontSize: 18,
      fontWeight: 'bold',
      color: '#C62828',
    },
    pizzaIcon: {
      width: 100,
      height: 100,
      marginTop: 10,
      resizeMode: 'contain',
    },
    faviconIcon: {
      width: 350,
      height: 350,
      marginTop: -40,
      alignSelf: 'center',
      resizeMode: 'contain',
    },
    caixaBranca: {
      backgroundColor: '#FFF',
      paddingHorizontal: 10,
      paddingVertical: 6,
      borderRadius: 10,
      marginVertical: 6,
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
      gap: 20,
    },
    colunaItem: {
      alignItems: 'center',
    },
    statusTexto: {
      fontWeight: 'bold',
      marginTop: 4,
      fontSize: 14,
    },
    statusEntregue: {
      color: '#00E676', // verde neon
    },
    statusCancelado: {
      color: '#FF1744', // vermelho vibrante
    },
    statusPendente: {
      color: '#FF9100', // laranja forte
    },
  });