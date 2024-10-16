window.ergoConnector = {
  nautilus: {
    connect: async () => {
      if (typeof ergo !== 'undefined') {
        try {
          const connected = await ergo.connect();
          return connected;
        } catch (error) {
          console.error("Failed to connect to Nautilus:", error);
          return false;
        }
      } else {
        console.error("Nautilus is not installed");
        return false;
      }
    },
    disconnect: async () => {
      if (typeof ergo !== 'undefined') {
        try {
          await ergo.disconnect();
        } catch (error) {
          console.error("Failed to disconnect from Nautilus:", error);
        }
      }
    }
  }
};