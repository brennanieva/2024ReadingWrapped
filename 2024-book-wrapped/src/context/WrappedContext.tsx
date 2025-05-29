import React, { createContext, useContext, useEffect, useState } from "react";

type WrappedMetrics = Record<string, any>; // You can refine this type later

const WrappedContext = createContext<WrappedMetrics | null>(null);

export const WrappedProvider = ({ children }: { children: React.ReactNode }) => {
  const [metrics, setMetrics] = useState<WrappedMetrics | null>(null);

  useEffect(() => {
  fetch("/wrapped_metrics.json")
    .then((res) => {
      if (!res.ok) throw new Error("Failed to fetch metrics");
      return res.json();
    })
    .then((data) => {
      console.log("Fetched metrics:", data);
      setMetrics(data);
    })
    .catch((err) => {
      console.error("Error loading wrapped metrics:", err);
    });
}, []);

  return (
    <WrappedContext.Provider value={metrics}>
      {children}
    </WrappedContext.Provider>
  );
};

export const useWrapped = () => {
  const context = useContext(WrappedContext);
  if (!context) {
    console.warn("useWrapped used outside of WrappedProvider");
  }
  return context;
};

