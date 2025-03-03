document.addEventListener("DOMContentLoaded", function() {
    const API_URL = "/gerar-estrutura";
    const toastContainer = document.createElement("div");
    toastContainer.id = "toastContainer";
    document.body.appendChild(toastContainer);

    function showToast(message, success = true) {
        const toast = document.createElement("div");
        toast.className = "toast " + (success ? "success-toast" : "error-toast");
        toast.innerText = message;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Alternar modo escuro
    document.getElementById("toggleTheme").addEventListener("click", function() {
        document.body.classList.toggle("dark-mode");
        showToast("Modo " + (document.body.classList.contains("dark-mode") ? "Escuro" : "Claro") + " ativado");
    });

    // Geração do código
    document.getElementById("generateBtn").addEventListener("click", async function(event) {
        event.preventDefault();
        const inputText = document.getElementById("inputText").value;

        if (!inputText.trim()) {
            showToast("⚠️ Por favor, digite uma estrutura antes de gerar o código!", false);
            return;
        }

        try {
            const response = await fetch(API_URL, {  
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estrutura: inputText })
            });

            const data = await response.json();
            if (response.ok) {
                document.getElementById("outputCode").textContent = data.codigo.replace(/\n/g, "\n");
                showToast("✅ Código gerado com sucesso!");
            } else {
                showToast("❌ Erro ao gerar código:\n" + (data.erro || "Erro desconhecido."), false);
            }
        } catch (error) {
            showToast("🚨 Erro ao conectar com o servidor!", false);
        }
    });

    // Baixar a estrutura pronta
    document.getElementById("downloadStructureBtn").addEventListener("click", async function() {
        const inputText = document.getElementById("inputText").value;

        if (!inputText.trim()) {
            showToast("⚠️ Por favor, digite uma estrutura antes de baixar!", false);
            return;
        }

        try {
            const response = await fetch("/baixar-estrutura", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estrutura: inputText })
            });

            if (response.ok) {
                const blob = await response.blob();
                const link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = "estrutura.zip";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                showToast("📥 Estrutura baixada com sucesso!");
            } else {
                const data = await response.json();
                showToast("❌ Erro ao baixar estrutura:\n" + (data.erro || "Erro desconhecido."), false);
            }
        } catch (error) {
            showToast("🚨 Erro ao conectar com o servidor!", false);
        }
    });

    // Copiar o código gerado
    document.getElementById("copyBtn").addEventListener("click", function() {
        const outputCode = document.getElementById("outputCode").textContent;
        if (!outputCode.trim()) {
            showToast("⚠️ Nenhum código gerado para copiar!", false);
            return;
        }

        navigator.clipboard.writeText(outputCode)
            .then(() => showToast("✅ Código copiado para a área de transferência!"))
            .catch(err => showToast("❌ Erro ao copiar código: " + err, false));
    });

    // Baixar o código gerado como arquivo
    document.getElementById("downloadBtn").addEventListener("click", function() {
        const outputCode = document.getElementById("outputCode").textContent;
        if (!outputCode.trim()) {
            showToast("⚠️ Nenhum código gerado para baixar!", false);
            return;
        }

        const blob = new Blob([outputCode], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "gerar_estrutura.py";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        showToast("📥 Download iniciado com sucesso!");
    });
});
