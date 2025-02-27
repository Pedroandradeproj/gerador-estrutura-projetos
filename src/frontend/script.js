document.addEventListener("DOMContentLoaded", function() {
    const API_URL = "https://gerador-estrutura-projetos-nrk2.onrender.com/gerar-estrutura"; // 🔹 Backend no Render

    // Botão para gerar estrutura
    document.getElementById("generateBtn").addEventListener("click", async function() {
        const inputText = document.getElementById("inputText").value;

        if (!inputText.trim()) {
            alert("Por favor, digite uma estrutura antes de gerar o código!");
            return;
        }

        try {
            const response = await fetch(API_URL, {  // 🔹 Agora a requisição é `POST`
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estrutura: inputText })
            });

            const data = await response.json();

            if (response.ok) {
                document.getElementById("outputCode").textContent = data.codigo.replace(/\n/g, "\n");
            } else {
                alert("Erro ao gerar código: " + (data.erro || "Erro desconhecido."));
            }
        } catch (error) {
            console.error("Erro ao gerar estrutura:", error);
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
            .catch(err => console.error("Erro ao copiar código:", err));
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
