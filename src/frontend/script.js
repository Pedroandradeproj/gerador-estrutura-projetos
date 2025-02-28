document.addEventListener("DOMContentLoaded", function() {
    const API_URL = "/gerar-estrutura"; // 🔹 Caminho relativo para o backend

    console.log("✅ O JavaScript foi carregado corretamente!");

    const generateBtn = document.getElementById("generateBtn");

    if (!generateBtn) {
        console.error("❌ ERRO: O botão 'generateBtn' não existe no DOM.");
        return;
    }

    generateBtn.addEventListener("click", async function(event) {
        event.preventDefault();

        console.log("➡️ Botão 'Gerar Estrutura' clicado!");

        const inputText = document.getElementById("inputText").value;

        if (!inputText.trim()) {
            alert("⚠️ Por favor, digite uma estrutura antes de gerar o código!");
            return;
        }

        console.log("➡️ Enviando requisição para API...");
        console.log("🔹 URL:", API_URL);
        console.log("🔹 Método: POST");
        console.log("🔹 Payload:", JSON.stringify({ estrutura: inputText }));

        try {
            const response = await fetch(API_URL, {  
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estrutura: inputText })
            });

            console.log("⬅️ Resposta recebida da API...");
            console.log("🔹 Status:", response.status);
            console.log("🔹 Headers:", response.headers);

            const data = await response.json();
            console.log("🔹 Resposta JSON:", data);

            if (response.ok) {
                document.getElementById("outputCode").textContent = data.codigo.replace(/\n/g, "\n");
                console.log("✅ Código gerado com sucesso!");
            } else {
                console.error("❌ Erro ao gerar código:", data.erro || "Erro desconhecido.");
                alert("❌ Erro ao gerar código:\n" + (data.erro || "Erro desconhecido."));
            }
        } catch (error) {
            console.error("🚨 Erro ao conectar com o servidor:", error);
            alert("🚨 Erro ao conectar com o servidor.");
        }
    });

    // Botão para copiar código (Alert para o usuário)
    document.getElementById("copyBtn").addEventListener("click", function() {
        const outputCode = document.getElementById("outputCode").textContent;
        
        if (!outputCode.trim()) {
            alert("⚠️ Nenhum código gerado para copiar!");
            console.warn("⚠️ O usuário tentou copiar sem ter código gerado.");
            return;
        }

        navigator.clipboard.writeText(outputCode)
            .then(() => alert("✅ Código copiado para a área de transferência!"))
            .catch(err => alert("❌ Erro ao copiar código: " + err));
    });

    // Botão para baixar código como .py (Alert para o usuário)
    document.getElementById("downloadBtn").addEventListener("click", function() {
        const outputCode = document.getElementById("outputCode").textContent;
        
        if (!outputCode.trim()) {
            alert("⚠️ Nenhum código gerado para baixar!");
            console.warn("⚠️ O usuário tentou baixar sem ter código gerado.");
            return;
        }

        const blob = new Blob([outputCode], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "gerar_estrutura.py";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        alert("📥 Download iniciado com sucesso!");
    });
});
