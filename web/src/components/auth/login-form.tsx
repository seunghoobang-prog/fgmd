"use client";

import { useState } from "react";
import { signIn } from "@/lib/actions/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

export function LoginForm() {
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);

    const form = new FormData(e.currentTarget);
    const email = form.get("email") as string;
    const password = form.get("password") as string;

    const result = await signIn(email, password);
    if (result && !result.success) {
      toast.error(result.error);
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        name="email"
        type="email"
        label="이메일"
        placeholder="name@company.com"
        required
        autoComplete="email"
      />
      <Input
        name="password"
        type="password"
        label="비밀번호"
        required
        autoComplete="current-password"
      />
      <Button type="submit" className="w-full" size="lg" loading={loading}>
        로그인
      </Button>
    </form>
  );
}