document.addEventListener("DOMContentLoaded", function() {
    const API_URL = "https://gerador-estrutura-projetos-nrk2.onrender.com/gerar-estrutura"; // 🔹 URL do backend no Render

    // Botão para gerar estrutura
    document.getElementById("generateBtn").addEventListener("click", async function(event) {
        event.preventDefault(); // 🔹 Evita comportamento padrão que pode estar acionando GET sem querer

        const inputText = document.getElementById("inputText").value;

        if (!inputText.trim()) {
            alert("Por favor, digite uma estrutura antes de gerar o código!");
            return;
        }

        console.log("➡️ [DEBUG] Enviando requisição para API...");
        console.log("🔹 [DEBUG] URL:", API_URL);
        console.log("🔹 [DEBUG] Método: POST");
        console.log("🔹 [DEBUG] Payload:", JSON.stringify({ estrutura: inputText }));

        try {
            const response = await fetch(API_URL, {  
                method: "POST",  // 🔹 Garantindo que é POST
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estrutura: inputText })
            });

            console.log("⬅️ [DEBUG] Resposta recebida da API...");
            console.log("🔹 [DEBUG] Status:", response.status);
            console.log("🔹 [DEBUG] Headers:", response.headers);

            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }

            const data = await response.json();
            console.log("🔹 [DEBUG] Resposta JSON:", data);

            if (response.ok) {
                document.getElementById("outputCode").textContent = data.codigo.replace(/\n/g, "\n");
                console.log("✅ [DEBUG] Código gerado com sucesso!");
            } else {
                console.error("❌ [DEBUG] Erro ao gerar código:", data.erro || "Erro desconhecido.");
                alert("Erro ao gerar código: " + (data.erro || "Erro desconhecido."));
            }
        } catch (error) {
            console.error("🚨 [DEBUG] Erro ao conectar com o servidor:", error);
            alert("Erro ao conectar com o servidor.");
        }
    });

    // Botão para copiar código
    document.getElementById("copyBtn").addEventListener("click", function() {
        const outputCode = document.getElementById("outputCode").textContent;
        
        if (!outputCode.trim()) {
            alert("Nenhum código gerado para copiar!");
            return;
        }

        navigator.clipboard.writeText(outputCode)
            .then(() => alert("Código copiado para a área de transferência!"))
            .catch(err => console.error("❌ [DEBUG] Erro ao copiar código:", err));
    });

    // Botão para baixar código como .py
    document.getElementById("downloadBtn").addEventListener("click", function() {
        const outputCode = document.getElementById("outputCode").textContent;
        
        if (!outputCode.trim()) {
            alert("Nenhum código gerado para baixar!");
            return;
        }

        const blob = new Blob([outputCode], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "gerar_estrutura.py";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
});
