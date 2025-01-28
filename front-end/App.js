import React, { useState, useEffect } from "react";
import Navigation from "./src/navigation/Navigation";
import { ThemeProvider } from "./src/context/ThemeContext";
import * as Font from "expo-font";
import { ActivityIndicator, View } from "react-native";

const App = () => {
  const [fontLoaded, setFontLoaded] = useState(false);

  useEffect(() => {
    async function loadFont() {
      await Font.loadAsync({
        "LuckiestGuy": require("./assets/fonts/LuckiestGuy.ttf"),
      });
      setFontLoaded(true);
    }

    loadFont();
  }, []);

  if (!fontLoaded) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <ThemeProvider>
      <Navigation />
    </ThemeProvider>
  );
};

export default App;

