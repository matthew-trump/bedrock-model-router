import { expect, test } from "@playwright/test";

test("loads models and submits a prompt through the local backend", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "Bedrock Model Router" })).toBeVisible();
  await expect(page.getByRole("combobox", { name: "Model" })).toContainText("Amazon Nova Lite");
  await expect(page.getByRole("combobox", { name: "Model" })).toContainText("Claude 3.5 Haiku");

  const modelSelector = page.getByRole("combobox", { name: "Model" });
  await modelSelector.selectOption("claude-haiku");
  await expect(modelSelector).toHaveValue("claude-haiku");
  await page.getByPlaceholder("Ask a model...").fill("hello from browser test");
  await page.getByRole("button", { name: "Send" }).click();

  const response = page.locator("pre");
  await expect(response).toContainText("Stub Bedrock response from anthropic.claude-3-5-haiku-20241022-v1:0");
  await expect(response).toContainText("hello from browser test");
});
