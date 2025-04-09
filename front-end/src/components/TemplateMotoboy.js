import React, { useEffect, useState } from "react";
import {
  View,
  StyleSheet,
  ImageBackground,
  Dimensions,
  ScrollView,
} from "react-native";
import { useTheme } from "../context/ThemeContext";

const TemplateMotoboy = ({ children }) => {
  const [isMobile, setIsMobile] = useState(false);
  const { isDarkMode } = useTheme();

  useEffect(() => {
    const updateLayout = () => {
      const width = Dimensions.get("window").width;
      setIsMobile(width < 768);
    };
    Dimensions.addEventListener("change", updateLayout);
    updateLayout();

    return () => {
      Dimensions.removeEventListener("change", updateLayout);
    };
  }, []);

  const styles = StyleSheet.create({
    containerPrincipal: {
      flex: 1,
      backgroundColor: isDarkMode ? "#000" : "#FFF",
    },
    backImage: {
      flex: 1,
      width: "100%",
      height: "100%",
    },
    scrollContainer: {
      flexGrow: 1,
      padding: 20,
      backgroundColor: isDarkMode ? "rgba(0, 0, 0, 0.17)" : "rgba(245, 236, 236, 0)",
    },
  });

  return (
    <View style={styles.containerPrincipal}>
      <ImageBackground
        source={require("../../assets/images/bg-opaco.png")}
        style={styles.backImage}
        resizeMode="cover"
      >
        <ScrollView
          contentContainerStyle={styles.scrollContainer}
          showsVerticalScrollIndicator={true}
          indicatorStyle={isDarkMode ? "white" : "black"}
        >
          {children}
        </ScrollView>
      </ImageBackground>
    </View>
  );
};

export default TemplateMotoboy;
